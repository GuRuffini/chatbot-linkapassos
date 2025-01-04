from chatbot.assistant import create_assistant

def create_thread():
    """
    Cria uma thread com o contexto inicial do assistente.
    """
    try:
        assistant = create_assistant()

        messages = [
            {"role": "system", "content": assistant.instructions}
        ]

        return messages
    except Exception as e:
        raise RuntimeError(f"Erro ao criar a thread: {e}")