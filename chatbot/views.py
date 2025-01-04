from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from chatbot.streaming import handle_message
import json

def index(request):
    """
    Renderiza a página inicial do chatbot.
    """
    return render(request, 'chatbot/index.html')

@csrf_exempt
def chat(request):
    """
    Processa a interação do chatbot.
    """
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            user_input = body.get('msg', '')

            if not user_input:
                return JsonResponse({'error': 'O campo "msg" é obrigatório.'}, status=400)

            resposta = handle_message(user_input)
            return JsonResponse({'resposta': resposta})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Método não permitido.'}, status=405)