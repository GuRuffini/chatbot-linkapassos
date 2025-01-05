from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from chatbot.streaming import handle_message
from chatbot.message import add_message
from chatbot.models import ChatHistory, Communication
import json
import markdown

class CustomLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return '/chatbot/'

def index(request):
    return render(request, 'registration/login.html')

@login_required
def chatbot_view(request):
    return render(request, 'chatbot.html')

@csrf_exempt
@require_POST
def chat(request):
    try:
        body = json.loads(request.body)
        user_input = body.get('msg', '').strip()

        if not user_input:
            return JsonResponse({'error': 'O campo "msg" é obrigatório.'}, status=400)

        session_id = request.session.session_key or request.session.create()

        chat_history, created = ChatHistory.objects.get_or_create(session_id=session_id)
        if not chat_history.messages:
            chat_history.messages = []

        communication_id = body.get('communication_id')
        if communication_id:
            try:
                communication = Communication.objects.get(id=communication_id)
                chat_history.communication = communication
            except Communication.DoesNotExist:
                pass

        messages = chat_history.messages
        messages = add_message("user", user_input, existing_messages=messages)

        for message in messages:
            if 'role' not in message or 'content' not in message:
                raise ValueError("Mensagem no histórico está malformada.")

        response_content = handle_message(messages)
        messages.append({"role": "assistant", "content": response_content})
        chat_history.messages = messages
        chat_history.save()

        response_html = markdown.markdown(response_content, extensions=['extra', 'sane_lists'])

        return JsonResponse({'resposta': response_html})

    except Exception:
        return JsonResponse({'error': 'Erro interno do servidor.'}, status=500)
