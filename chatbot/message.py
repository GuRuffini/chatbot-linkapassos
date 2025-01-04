from chatbot.thread import create_thread

def add_message(role, content):
    """
    Adiciona uma mensagem ao contexto da thread.
    
    Args:
        role (str): O papel da mensagem (e.g., "user", "assistant").
        content (str): O conteúdo da mensagem.
    
    Returns:
        list: Histórico atualizado da thread.
    """
    messages = create_thread()
    messages.append({"role": role, "content": content})
    return messages
