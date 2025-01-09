from flask import Blueprint, request, jsonify
from services.faiss_service import search_embedding
from services.openai_service import generate_response
from utils.config import model, collection

chat_routes = Blueprint('chat', __name__)

@chat_routes.route('/chat', methods=['POST'])
def chat():
    query = request.json.get('query')
    if not query:
        return jsonify({"error": "A consulta não pode estar vazia."}), 400

    query_embedding = model.encode(query).reshape(1, -1)
    distances, indices = search_embedding(query_embedding)

    if distances[0][0] < 1.5:
        doc_id = list(collection.find({}, {"_id": 1}))[int(indices[0][0])]["_id"]
        doc = collection.find_one({"_id": doc_id})
        context = doc['text']
        response = generate_response(query, context)
        return jsonify({"response": response})

    return jsonify({"response": "Desculpe, não encontrei informações relevantes."})
