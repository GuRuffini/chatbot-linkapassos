from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from openai import OpenAI
from dotenv import load_dotenv
import json
import os

load_dotenv()

cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def index(request):
    return render(request, 'chatbot/index.html')

@csrf_exempt
def chat(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            prompt = body.get('msg', '')
            
            if not prompt:
                return JsonResponse({'error': 'O campo "msg" é obrigatório.'}, status=400)
            
            resposta = cliente.completions.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=100
            )
            
            return JsonResponse({'resposta': resposta.choices[0].text.strip()})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Método não permitido.'}, status=405)