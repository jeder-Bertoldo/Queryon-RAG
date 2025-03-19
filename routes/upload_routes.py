from flask import Blueprint, request, jsonify, render_template
from services.pdf_service import extract_text_from_pdf
from services.faiss_service import add_embedding
from utils.config import collection, model
from services.scraper_service import process_resolutions
from services.faiss_retrieval import get_relevant_chunks


upload_routes = Blueprint('upload', __name__)  # ✅ Definido apenas uma vez!

@upload_routes.route('/')
def index():
    return render_template('index.html')

@upload_routes.route('/upload', methods=['POST'])
def upload_documents():
    files = request.files.getlist('files')  # Aceitar múltiplos arquivos
    if not files:
        return jsonify({"error": "Nenhum arquivo enviado."}), 400

    total_documents = 0

    for file in files:
        # Extrair texto do arquivo atual
        text = extract_text_from_pdf(file)

        # Verifica se já existe esse texto no MongoDB
        if collection.find_one({"text": text}):
            print("⚠ Documento já existe no banco, ignorando...")
            continue  # Pula para o próximo arquivo

        # Gerar embedding para o texto
        embedding = model.encode(text).tolist()

        # Salvar no MongoDB
        document = {"text": text, "embedding": embedding}
        result = collection.insert_one(document)

        # Adicionar ao FAISS e salvar índice associado
        faiss_index_id = add_embedding(embedding)
        collection.update_one({"_id": result.inserted_id}, {"$set": {"faiss_index": faiss_index_id}})

        total_documents += 1

    return jsonify({"message": f"{total_documents} documentos adicionados com sucesso!"})

@upload_routes.route('/scrape_all', methods=['GET'])
def scrape_all():
    """
    Percorre todas as resoluções do IFAC e armazena no MongoDB sem duplicação.
    """
    result = process_resolutions()
    return jsonify(result)




chat_routes = Blueprint('chat', __name__)

@chat_routes.route('/chat', methods=['POST'])
def chat():
    """
    Rota para processar a pergunta do usuário e buscar as melhores respostas no FAISS.
    """
    data = request.json
    query = data.get("question")

    if not query:
        return jsonify({"error": "Pergunta não pode estar vazia."}), 400

    relevant_chunks = get_relevant_chunks(query, top_k=3)

    if not relevant_chunks:
        return jsonify({"message": "Nenhuma resposta relevante encontrada."})

    return jsonify({"responses": relevant_chunks})
