from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import render
from chatbot.streaming import handle_message
from chatbot.message import add_message
from chatbot.models import ChatHistory, Communication
import json
import markdown
import logging

logger = logging.getLogger(__name__)

def index(request):
    """
    Renderiza a página inicial.
    """
    return render(request, 'chatbot/index.html')

def chatbot_view(request):
    """
    Renderiza a página do chatbot.
    """
    return render(request, 'chatbot/chatbot.html')

@csrf_exempt
@require_POST
def chat(request):
    """
    Processa a interação do chatbot e persiste o histórico no banco de dados.
    """
    try:
        body = json.loads(request.body)
        user_input = body.get('msg', '').strip()
        logger.info(f'Entrada do usuário: {user_input}')

        if not user_input:
            return JsonResponse({'error': 'O campo "msg" é obrigatório.'}, status=400)

        session_id = request.session.session_key or request.session.create()
        logger.info(f"ID da sessão: {session_id}")

        # Recupera ou cria o histórico no banco
        chat_history, created = ChatHistory.objects.get_or_create(session_id=session_id)
        if not chat_history.messages:
            chat_history.messages = []  # Inicializa o campo com uma lista vazia

        # Recupera o tom de comunicação (opcional)
        communication_id = body.get('communication_id')
        if communication_id:
            try:
                communication = Communication.objects.get(id=communication_id)
                chat_history.communication = communication
                logger.info(f"Tom de comunicação associado: {communication}")
            except Communication.DoesNotExist:
                logger.warning(f"Tom de comunicação {communication_id} não encontrado.")

        # Adiciona a mensagem do usuário ao histórico
        messages = chat_history.messages
        messages = add_message("user", user_input, existing_messages=messages)

        # Validação adicional para mensagens
        for message in messages:
            if 'role' not in message or 'content' not in message:
                logger.error(f"Mensagem malformada: {message}")
                raise ValueError("Mensagem no histórico está malformada.")

        # Processa a mensagem no backend
        response_content = handle_message(messages)

        # Adiciona a resposta ao histórico
        messages.append({"role": "assistant", "content": response_content})
        chat_history.messages = messages
        chat_history.save()

        # Renderiza a resposta como Markdown
        response_html = markdown.markdown(response_content, extensions=['extra', 'sane_lists'])

        return JsonResponse({'resposta': response_html})

    except Exception as e:
        logger.error(f"Erro ao processar a mensagem: {e}")
        return JsonResponse({'error': 'Erro interno do servidor.'}, status=500)