import json
import markdown
import logging
import re
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import messages
from chatbot.streaming import handle_message
from chatbot.message import add_message
from chatbot.models import ChatHistory, Communication

logger = logging.getLogger(__name__)


class CustomLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return '/chatbot/'

    def form_invalid(self, form):
        """
        Este método é chamado quando o formulário de login é inválido.
        """
        username = self.request.POST.get('username', '').strip()
        password = self.request.POST.get('password', '').strip()

        if not username:
            messages.error(self.request, "O campo 'Usuário' não pode estar vazio.")
        elif not re.match(r'^[a-zA-Z0-9_.@-]{3,50}$', username):
            messages.error(self.request, "O nome de usuário deve conter apenas caracteres válidos (letras, números, '_', '.', '@', '-') e ter entre 3 e 50 caracteres.")

        if not password:
            messages.error(self.request, "O campo 'Senha' não pode estar vazio.")
        elif len(password) < 8 or len(password) > 100:
            messages.error(self.request, "A senha deve ter entre 8 e 100 caracteres.")
        elif not re.match(r'(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$', password):
            messages.error(self.request, "A senha deve conter pelo menos uma letra maiúscula, uma minúscula, um número e um caractere especial.")

        messages.error(self.request, "Credenciais inválidas. Verifique o nome de usuário e senha.")
        return self.render_to_response(self.get_context_data(form=form))


def index(request):
    return render(request, 'registration/login.html')


@login_required
def chatbot_view(request):
    return render(request, 'chatbot.html')


@require_POST
def chat(request):
    try:
        body = json.loads(request.body)
        user_input = body.get('msg', '').strip()

        if not user_input:
            return JsonResponse({'error': 'O campo "msg" é obrigatório.'}, status=400)

        session_id = request.session.session_key or request.session.create()

        try:
            chat_history, created = ChatHistory.objects.get_or_create(session_id=session_id)
            if not chat_history.messages:
                chat_history.messages = []
        except Exception as e:
            logger.error(f"Erro ao acessar histórico de chat: {e}")
            return JsonResponse({'error': 'Erro ao acessar o histórico de chat.'}, status=500)

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

    except Exception as e:
        logger.error(f"Erro no endpoint /chat/: {str(e)}")
        return JsonResponse({'error': 'Erro interno do servidor.'}, status=500)
