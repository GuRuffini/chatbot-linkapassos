from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import path, include
from chatbot.views import chatbot_view

def index_redirect(request):
    if request.user.is_authenticated:
        return redirect('chatbot')
    return redirect('login')

urlpatterns = [
    path('', index_redirect, name='index'),
    path('', include('django.contrib.auth.urls')),
    path('chatbot/', login_required(chatbot_view), name='chatbot'),
]
