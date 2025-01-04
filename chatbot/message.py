from chatbot.thread import create_thread

def add_message(role, content, existing_messages=None):
    """
    Adiciona uma mensagem ao contexto da thread.
    
    Args:
        role (str): O papel da mensagem (e.g., "user", "assistant").
        content (str): O conteúdo da mensagem.
        existing_messages (list): Histórico de mensagens existente.
    
    Returns:
        list: Histórico atualizado da thread.
    """
    messages = create_thread(existing_messages)
    messages.append({"role": role, "content": content})
    return messages
