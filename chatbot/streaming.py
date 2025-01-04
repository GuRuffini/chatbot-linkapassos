from chatbot.message import add_message
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def handle_message(user_input):
    """
    Processa uma mensagem do usuário e retorna a resposta do assistente com efeito de streaming.
    
    Args:
        user_input (str): Entrada do usuário.
    
    Returns:
        str: Resposta completa do assistente.
    """
    try:
        messages = add_message("user", user_input)

        response_content = ""
        print("Resposta (em streaming):", end=" ", flush=True)
        
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

        messages.append({"role": "assistant", "content": response_content})

        return response_content
    except Exception as e:
        raise RuntimeError(f"Erro no processamento da mensagem: {e}")
