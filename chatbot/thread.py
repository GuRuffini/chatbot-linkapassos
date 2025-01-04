from chatbot.assistant import create_assistant

def create_thread(existing_messages=None):
    """
    Cria ou recupera uma thread com o contexto do assistente.
    """
    try:
        assistant = create_assistant()

        messages = existing_messages or [{"role": "system", "content": assistant.instructions}]

        return messages
    except Exception as e:
        raise RuntimeError(f"Erro ao criar a thread: {e}")