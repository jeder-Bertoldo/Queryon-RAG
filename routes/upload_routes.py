from flask import Blueprint, request, jsonify, render_template
from services.pdf_service import extract_text_from_pdf
from services.faiss_service import add_embedding
from utils.config import collection, model

upload_routes = Blueprint('upload', __name__)

@upload_routes.route('/')
def index():
    return render_template('index.html')

@upload_routes.route('/upload', methods=['POST'])
def upload_document():
    file = request.files.get('file')
    if not file:
        return jsonify({"error": "Nenhum arquivo enviado."}), 400

    text = extract_text_from_pdf(file)
    embedding = model.encode(text).tolist()

    # Salvar no MongoDB
    document = {"text": text, "embedding": embedding}
    result = collection.insert_one(document)

    # Adicionar ao FAISS e salvar índice associado
    faiss_index_id = add_embedding(embedding)
    collection.update_one({"_id": result.inserted_id}, {"$set": {"faiss_index": faiss_index_id}})

    return jsonify({"message": "Documento adicionado com sucesso!"})
