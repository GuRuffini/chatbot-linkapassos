from django.utils.timezone import localtime
from django.contrib import admin
from .models import Assistant, Role, Communication


@admin.register(Assistant)
class AssistantAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'model', 'created_at')
    list_display_links = ('id', 'name')
    list_filter = ('is_active',)
    search_fields = ('name', 'model')
    ordering = ('id',)
    readonly_fields = ('id', 'user', 'created_at', 'updated_at')
    fieldsets = (
        ('Informações Básicas', {
            'fields': (
                'instructions',
                'name',
                'model',
                'is_active'
            )
        }),
    )


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'assistent', 'created_at')
    list_display_links = ('id', 'name')
    list_filter = ('is_active',)
    search_fields = ('name', 'objective')
    ordering = ('id',)
    readonly_fields = ('id', 'user', 'created_at', 'updated_at')
    fieldsets = (
        ('Informações Básicas', {
            'fields': (
                'assistent',
                'name',
                'description',
                'objective',
                'is_active'
            )
        }),
    )


@admin.register(Communication)
class CommunicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'tone', 'assistent', 'created_at')
    list_display_links = ('tone',)
    list_filter = ('is_active',)
    search_fields = ('tone', 'assistent')
    ordering = ('id',)
    readonly_fields = ('id', 'user', 'created_at', 'updated_at')
    fieldsets = (
        ('Informações Básicas', {
            'fields': (
                'assistent',
                'tone',
                'vocabulary',
                'is_active'
            )
        }),
    )