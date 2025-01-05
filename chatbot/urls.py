from django.urls import path
from .views import CustomLoginView, chatbot_view, chat

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('chatbot/', chatbot_view, name='chatbot'),
    path('chat/', chat, name='chat'),
]
