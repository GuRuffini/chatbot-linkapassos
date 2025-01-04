from django.db.models.signals import pre_save
from django.dispatch import receiver
from chatbot.models import Assistant, Role, Communication
from threading import local

_user = local()

def set_current_user(user):
    _user.value = user

def get_current_user():
    return getattr(_user, 'value', None)

@receiver(pre_save, sender=Assistant)
@receiver(pre_save, sender=Role)
@receiver(pre_save, sender=Communication)
def definir_usuario_logado(sender, instance, **kwargs):
    current_user = get_current_user()
    if current_user and not instance.user:
        instance.user = current_user