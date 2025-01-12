from flask import Blueprint, request, jsonify, render_template
from services.pdf_service import extract_text_from_pdf
from services.faiss_service import add_embedding
from utils.config import collection, model

upload_routes = Blueprint('upload', __name__)

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
