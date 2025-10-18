from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin customizado para o modelo User"""
    
    list_display = ('username', 'email', 'user_type', 'verified', 'followers_count', 'date_joined')
    list_filter = ('user_type', 'verified', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Informações Adicionais', {
            'fields': ('user_type', 'bio', 'avatar', 'phone', 'birth_date', 'location', 'verified', 'followers_count')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Informações Adicionais', {
            'fields': ('user_type', 'email', 'first_name', 'last_name')
        }),
    )
