from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
import openai
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente
load_dotenv()

# Configuração do app
app = Flask(__name__)

# Configuração do MongoDB
MONGO_URI = os.getenv('MONGO_URI', 'MONGO_URI=mongodb://localhost:27017/chatbot_db/vectors')
client = MongoClient(MONGO_URI)
db = client['resolucoes']
collection = db['documentos']

# Modelo de embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')

# Configuração FAISS
d = 384  # Dimensão dos embeddings
faiss_index = faiss.IndexFlatL2(d)

# Configuração OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

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
        faiss_index.add(np.array([embedding]))
        return jsonify({"message": "Documento adicionado com sucesso!"})
    return jsonify({"error": "Nenhum arquivo enviado."})

@app.route('/chat', methods=['POST'])
def chat():
    query = request.json['query']
    query_embedding = model.encode(query).reshape(1, -1)
    distances, indices = faiss_index.search(query_embedding, 1)
    
    if distances[0][0] < 0.5:  # Ajuste do limite
        doc = collection.find_one()
        context = doc['text']
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um assistente que responde com base no contexto fornecido."},
                {"role": "user", "content": f"Contexto: {context}\nPergunta: {query}"}
            ]
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
