import os
import sys
from django.core.wsgi import get_wsgi_application

sys.path.append('/home/exata-dev/chatbot-linkapassos')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

get_wsgi_application()

from chatbot.models import Assistant
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def create_assistant():
    try:
        assistant_instance = Assistant.objects.filter(is_active=True, id=1).first()

        if not assistant_instance:
            raise ValueError("Assistant com ID 1 não encontrado ou não está ativo.")

        created_assistant = client.beta.assistants.create(
            instructions=assistant_instance.instructions,
            name=assistant_instance.name,
            model=assistant_instance.model
        )

        return created_assistant
    except Exception as e:
        raise RuntimeError(f"Erro ao criar o assistente: {e}")

try:
    car_sales_assistant = create_assistant()
    print("Instructions:", car_sales_assistant.instructions)
    print("Name:", car_sales_assistant.name)
    print("Model:", car_sales_assistant.model)
except Exception as e:
    print(str(e))
