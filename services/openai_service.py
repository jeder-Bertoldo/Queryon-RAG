import openai
from utils.config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def generate_response(query, context):
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "Você é o agente inteligente queryon e vai responder as perguntas com base do texto disponivel"},
            {"role": "user", "content": f"Contexto: {context}\nPergunta: {query}"}
        ]
    )
    return response['choices'][0]['message']['content']
