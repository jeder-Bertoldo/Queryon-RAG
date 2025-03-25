import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import re

# Configuração do MongoDB
MONGO_URI = "mongodb://localhost:27017/"
client = MongoClient(MONGO_URI)
db = client["chatbot_db"]
vectors_collection = db["vectors"]

# Configuração do modelo de embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")

# Configuração do FAISS
embedding_size = 384  # Tamanho do vetor do modelo
faiss_index = faiss.IndexFlatL2(embedding_size)

# Cabeçalhos para evitar bloqueio de scraping
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"}

def split_text_into_chunks(text, max_words=300):
    """
    Divide um texto grande em partes menores (chunks) sem cortar frases no meio.
    
    :param text: Texto a ser dividido
    :param max_words: Número máximo de palavras por chunk
    :return: Lista de chunks organizados
    """
    sentences = re.split(r'(?<=[.!?])\s+', text)  # Divide o texto em frases
    chunks = []
    current_chunk = []
    current_word_count = 0

    for sentence in sentences:
        words = sentence.split()
        if current_word_count + len(words) > max_words:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_word_count = 0
        current_chunk.append(sentence)
        current_word_count += len(words)

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

def extract_resolution_text(url):
    """Extrai o conteúdo da resolução a partir da URL."""
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        print(f"❌ Erro ao acessar {url}")
        return None, None
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Extrai o título
    title = soup.find("h1", class_="documentFirstHeading")
    title = title.get_text(strip=True) if title else "Título Desconhecido"
    
    # Extrai o conteúdo principal
    content_div = soup.find("div", id="content-core")
    if not content_div:
        print(f"⚠️ Conteúdo não encontrado em {url}")
        return title, None
    
    paragraphs = content_div.find_all("p")
    text = "\n".join([p.get_text(strip=True) for p in paragraphs])
    
    return title, text

# limitação de resoluções
def process_resolutions(base_url, max_resolutions=3):
    """Percorre os anos e baixa resoluções até atingir o limite."""
    total_downloaded = 0

    # Acessa a página principal para obter os anos disponíveis
    response = requests.get(base_url, headers=HEADERS)
    if response.status_code != 200:
        print("❌ Erro ao acessar a página principal de resoluções.")
        return
    
    soup = BeautifulSoup(response.text, "html.parser")
    year_links = soup.select("a.internal-link")

    print("🔍 Analisando anos disponíveis...")
    for link in year_links:
        year_url = link["href"]
        if not year_url.startswith("http"):
            year_url = base_url + year_url  # Corrige URL relativa
        print(f"📌 Ano encontrado: {year_url}")

        # Acessa a página do ano específico
        year_response = requests.get(year_url, headers=HEADERS)
        if year_response.status_code != 200:
            print(f"❌ Erro ao acessar {year_url}")
            continue
        
        year_soup = BeautifulSoup(year_response.text, "html.parser")
        resolution_links = year_soup.select("a.internal-link")

        print(f"🔍 Resoluções encontradas para {year_url}:")
        for res_link in resolution_links:
            res_url = res_link["href"]
            if not res_url.startswith("http"):
                res_url = base_url + res_url

            print(f"➡️ Verificando resolução: {res_url}")

            # Verifica se a resolução já está no banco
            if vectors_collection.find_one({"url": res_url}):
                print(f"⚠️ Resolução já armazenada: {res_url}")
                continue

            title, text = extract_resolution_text(res_url)
            if text:
                # 🔹 Divide o texto em partes menores (chunks)
                chunks = split_text_into_chunks(text, max_words=300)

                for i, chunk in enumerate(chunks):
                    # Gerar embedding para cada chunk
                    embedding = model.encode(chunk).tolist()

                    # Salvar cada chunk no MongoDB
                    document = {
                        "title": title,
                        "chunk_index": i,
                        "text": chunk,
                        "embedding": embedding,
                        "url": res_url
                    }
                    vectors_collection.insert_one(document)

                    # Adicionar ao FAISS
                    embedding_array = np.array([embedding], dtype=np.float32)
                    faiss_index.add(embedding_array)

                    print(f"✅ Chunk {i+1} de '{title}' armazenado no MongoDB e FAISS.")
                
                total_downloaded += 1


                # Se atingiu o limite, para o processo
                if total_downloaded >= max_resolutions:
                    print("🔹 Limite de resoluções atingido. Finalizando processo.")
                    return

# URL base das resoluções do IFAC
base_url = "https://www.ifac.edu.br/orgaos-colegiados/conselhos/consu/resolucoes"

# Executa o processo
process_resolutions(base_url)
