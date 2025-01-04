from django.db import models
from django.contrib.auth.models import User


class Assistant(models.Model):
    MODEL_CHOICES = [
        ('gpt-4o', 'gpt-4o'),
        ('gpt-4o-mini', 'gpt-4o-mini'),
    ]

    instructions = models.TextField(blank=False, null=False, verbose_name="Instruções", help_text="Diretrizes que definem o comportamento e objetivo do assistente.")
    name = models.CharField(max_length=15, unique=True, blank=False, null=False, verbose_name="Nome", help_text="Identificação única do assistente (máximo de 15 caracteres).")
    model = models.CharField(max_length=30, choices=MODEL_CHOICES, blank=False, null=False, verbose_name="Modelo", help_text="Escolha o tipo ou versão do modelo de IA a ser usado.")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Atualização")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="assistants", verbose_name="Usuário")
    is_active = models.BooleanField(default=True, verbose_name="Ativo", help_text="Indica se o assistente está ativo para uso.")

    class Meta:
        app_label = 'chatbot'
        verbose_name = "Assistente"
        verbose_name_plural = "Assistentes"
        ordering = ['id']
        db_table = 'chatbot_assistant'

    def __str__(self):
        return self.name
    

class Role(models.Model):
    assistent = models.ForeignKey(Assistant, on_delete=models.CASCADE, related_name="roles_for_user", verbose_name="Assistente")
    name = models.CharField(max_length=30, blank=False, null=False, verbose_name="Regra", help_text="Escreva o nome da regra.")
    description = models.TextField(verbose_name="Descrição do Papel", help_text="Defina o papel principal e as responsabilidades do agente.")
    objective = models.TextField(verbose_name="Objetivo Principal", help_text="Especifique o objetivo final do agente nesta interação.")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Atualização")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="roles_by_user", verbose_name="Usuário")
    is_active = models.BooleanField(default=True, verbose_name="Ativo", help_text="Indica se o assistente está ativo para uso.")

    class Meta:
        app_label = 'chatbot'
        verbose_name = "Regra"
        verbose_name_plural = "Regras"
        ordering = ['id']
        db_table = 'chatbot_role'

    def __str__(self):
        return self.name


class Communication(models.Model):
    TONE = [
        ('CASUAL', 'Casual'),
        ('FORMAL', 'Formal'),
        ('DIRETO AO PONTO', 'Direto ao Ponto'),
        ('AMIGAVEL', 'Amigável'),
        ('PROFISSIONAL', 'Profissional'),
        ('PERSUASIVO', 'Persuasivo'),
        ('INFORMATIVO', 'Informativo'),
        ('MOTIVADOR', 'Motivador'),
        ('NEUTRO', 'Neutro'),
        ('EMPATICO', 'Empático'),
    ]

    assistent = models.ForeignKey(Assistant, on_delete=models.CASCADE, related_name="communications", verbose_name="Assistente")
    tone = models.CharField(max_length=50, choices=TONE, blank=False, null=False, verbose_name="Tom de Comunicação", help_text="Exemplo: casual, formal, direto ao ponto, etc.")
    vocabulary = models.TextField(verbose_name="Vocabulário e Abordagem", help_text="Descreva o vocabulário e a abordagem que o agente deve usar.")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Atualização")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="communications_by_user", verbose_name="Usuário")
    is_active = models.BooleanField(default=True, verbose_name="Ativo", help_text="Indica se o assistente está ativo para uso.")

    class Meta:
        app_label = 'chatbot'
        verbose_name = "Tom de Comunicação"
        verbose_name_plural = "Tons de Comunicação"
        ordering = ['id']
        db_table = 'chatbot_communication'

    def __str__(self):
        return self.tone


class ChatHistory(models.Model):
    session_id = models.CharField(max_length=255, unique=True, verbose_name="ID da Sessão", help_text="Identificador único da sessão do usuário.")
    messages = models.JSONField(default=list, verbose_name="Histórico de Mensagens", help_text="Armazena o histórico completo de mensagens em formato JSON.")
    communication = models.ForeignKey('chatbot.Communication', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Tom de Comunicação", help_text="Define o tom de comunicação usado nessa sessão.")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação", help_text="Data em que o histórico foi criado.")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Atualização", help_text="Data da última atualização no histórico.")

    class Meta:
        app_label = 'chatbot'
        verbose_name = "Histórico de Conversa"
        verbose_name_plural = "Históricos de Conversa"
        ordering = ['-created_at']
        db_table = 'chatbot_chat_history'

    def __str__(self):
        return f"Histórico da Sessão {self.session_id}"