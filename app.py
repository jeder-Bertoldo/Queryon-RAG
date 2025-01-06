from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
import openai
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import os
from bson.json_util import dumps

# Carregar variáveis de ambiente
load_dotenv()

# Configuração do Flask
app = Flask(__name__)

# Configuração do MongoDB
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)
db = client["chatbot_db"]
collection = db["vectors"]

# Modelo de embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")

# Configuração do índice FAISS
d = 384
faiss_index = faiss.IndexFlatL2(d)

# Configuração da API OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Inicializar o FAISS na primeira requisição
@app.before_request
def initialize_faiss_once():
    if not hasattr(app, 'faiss_initialized'):
        print("Carregando embeddings no FAISS...")
        response = load_embeddings()
        print(response.get_json())
        app.faiss_initialized = True

@app.route('/load_embeddings', methods=['GET'])
def load_embeddings():
    documents = collection.find()
    embeddings = []
    
    for doc in documents:
        embedding = doc.get("embedding")
        if embedding:
            embeddings.append(np.array(embedding, dtype=np.float32))
    
    if embeddings:
        embeddings_array = np.vstack(embeddings)
        faiss_index.add(embeddings_array)
        print(f"Total de embeddings carregados no FAISS: {faiss_index.ntotal}")
        return jsonify({"message": f"{len(embeddings)} embeddings carregados no FAISS."})
    else:
        print("Nenhum embedding encontrado no MongoDB.")
        return jsonify({"error": "Nenhum embedding encontrado no MongoDB."})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_document():
    file = request.files['file']
    if file:
        text = extract_text_from_pdf(file)
        embedding = model.encode(text).tolist()
        document = {"text": text, "embedding": embedding}
        collection.insert_one(document)
        embedding_array = np.array([embedding], dtype=np.float32)
        faiss_index.add(embedding_array)
        print(f"Total de embeddings no FAISS após adição: {faiss_index.ntotal}")
        return jsonify({"message": "Documento adicionado com sucesso!"})
    return jsonify({"error": "Nenhum arquivo enviado."})

@app.route('/chat', methods=['POST'])
def chat():
    query = request.json['query']
    query_embedding = model.encode(query).reshape(1, -1)
    distances, indices = faiss_index.search(query_embedding, 1)
    print(f"Distâncias encontradas: {distances}, Índices encontrados: {indices}")
    
    if distances[0][0] < 1.5:
        doc_id = list(collection.find({}, {"_id": 1}))[indices[0][0]]["_id"]
        doc = collection.find_one({"_id": doc_id})
        print(f"Documento relevante encontrado: {doc}")
        context = doc['text']
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um assistente que responde com base no contexto fornecido."},
                {"role": "user", "content": f"Contexto: {context}\nPergunta: {query}"}
            ],
            temperature=0.7  # Parâmetro opcional para controle de criatividade
        )
        return jsonify({"response": response['choices'][0]['message']['content']})
    return jsonify({"response": "Desculpe, não encontrei informações relevantes."})

def extract_text_from_pdf(pdf_file):
    from PyPDF2 import PdfReader
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

if __name__ == '__main__':
    app.run(debug=True)
