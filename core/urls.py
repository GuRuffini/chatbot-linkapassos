from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from chatbot.views import chatbot_view

def index_redirect(request):
    if request.user.is_authenticated:
        return redirect('chatbot')
    return redirect('login')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_redirect, name='index'),
    path('', include('django.contrib.auth.urls')),
    path('chatbot/', chatbot_view, name='chatbot'),
    path('chat/', include('chatbot.urls')),
]
