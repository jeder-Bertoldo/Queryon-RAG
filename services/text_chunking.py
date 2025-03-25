import re

def split_text_into_chunks(text, max_words=800):
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
