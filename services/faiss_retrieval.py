import faiss
import numpy as np
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer

# Configuração do MongoDB
MONGO_URI = "mongodb://localhost:27017/"
client = MongoClient(MONGO_URI)
db = client["chatbot_db"]
vectors_collection = db["vectors"]

# Configuração do modelo de embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")

# Configuração do FAISS
embedding_size = 384
faiss_index = faiss.IndexFlatL2(embedding_size)  # Índice de busca por similaridade

def get_relevant_chunks(query, top_k=3):
    """
    Busca os chunks mais relevantes no FAISS e agrupa trechos vizinhos do mesmo documento.
    """
    query_embedding = model.encode(query).reshape(1, -1)
    distances, indices = faiss_index.search(query_embedding, top_k)  # Retorna os top_k chunks mais próximos

    results = []
    for idx in indices[0]:
        if idx == -1:
            continue
        doc = vectors_collection.find_one({"embedding": {"$exists": True}}, skip=idx, limit=1)
        if doc:
            results.append(doc)

    # Agrupar os chunks que pertencem ao mesmo documento
    grouped_results = {}
    for result in results:
        doc_id = result["url"]  # Usa a URL como identificador único do documento original
        if doc_id not in grouped_results:
            grouped_results[doc_id] = []
        grouped_results[doc_id].append(result["text"])

    # Unir os trechos vizinhos para dar mais contexto
    final_responses = []
    for doc_id, chunks in grouped_results.items():
        response_text = " ".join(chunks)  # Junta os trechos do mesmo documento
        final_responses.append({"url": doc_id, "text": response_text})

    return final_responses
