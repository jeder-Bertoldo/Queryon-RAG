import faiss
import numpy as np
from utils.config import collection

d = 384
faiss_index = faiss.IndexFlatL2(d)

def initialize_faiss():
    """Carrega os embeddings do MongoDB para o índice FAISS."""
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
    else:
        print("Nenhum embedding encontrado no MongoDB.")

def add_embedding(embedding):
    """Adiciona um embedding ao índice FAISS."""
    embedding_array = np.array([embedding], dtype=np.float32)
    faiss_index.add(embedding_array)

def search_embedding(query_embedding, top_k=1):
    """Realiza a busca por similaridade no índice FAISS."""
    distances, indices = faiss_index.search(query_embedding, top_k)
    return distances, indices
