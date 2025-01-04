from chatbot.message import add_message
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def handle_message(messages):
    """
    Processa uma mensagem do usuário e retorna a resposta do assistente com efeito de streaming.
    
    Args:
        messages (list): Histórico de mensagens, incluindo mensagens do usuário e do assistente.
    
    Returns:
        str: Resposta completa do assistente.
    """
    try:
        # Validação do histórico de mensagens
        for message in messages:
            if 'role' not in message or 'content' not in message:
                raise ValueError("Cada mensagem deve conter as chaves 'role' e 'content'.")
            if message['role'] not in ['user', 'assistant', 'system']:
                raise ValueError(f"Valor inválido para 'role': {message['role']}.")
            if not message['content']:
                raise ValueError("O campo 'content' não pode estar vazio.")

        response_content = ""
        print("Resposta (em streaming):", end=" ", flush=True)
        
        # Envio para a API OpenAI
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            stream=True
        )

        for chunk in stream:
            if chunk.choices[0].delta.content:
                delta = chunk.choices[0].delta.content
                response_content += delta
                print(delta, end="", flush=True)

        print("\n")

        return response_content
    except Exception as e:
        raise RuntimeError(f"Erro no processamento da mensagem: {e}")
