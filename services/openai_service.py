import openai
from utils.config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def generate_response(query, context):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um assistente que responde com base no contexto fornecido."},
            {"role": "user", "content": f"Contexto: {context}\nPergunta: {query}"}
        ]
    )
    return response['choices'][0]['message']['content']
