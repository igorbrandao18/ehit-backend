#!/usr/bin/env python
"""
Script para popular gêneros iniciais baseados nas choices existentes
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ehit_backend.settings')
django.setup()

from apps.genres.models import Genre
from apps.constants import GENRE_CHOICES

def create_genres():
    """Cria gêneros baseados nas choices existentes"""
    print("🎵 Criando gêneros musicais...")
    
    created_count = 0
    updated_count = 0
    
    for genre_key, genre_name in GENRE_CHOICES:
        genre, created = Genre.objects.get_or_create(
            slug=genre_key,
            defaults={
                'name': genre_name,
                'description': f'Gênero musical: {genre_name}',
                'color': '#FF6B6B',  # Cor padrão
                'is_active': True
            }
        )
        
        if created:
            created_count += 1
            print(f"✅ Criado: {genre_name}")
        else:
            updated_count += 1
            print(f"🔄 Já existe: {genre_name}")
    
    print(f"\n📊 Resumo:")
    print(f"   • Gêneros criados: {created_count}")
    print(f"   • Gêneros existentes: {updated_count}")
    print(f"   • Total de gêneros: {Genre.objects.count()}")

def create_subgenres():
    """Cria alguns subgêneros como exemplo"""
    print("\n🎶 Criando subgêneros...")
    
    # Buscar gêneros principais
    forro = Genre.objects.filter(slug='forro').first()
    sertanejo = Genre.objects.filter(slug='sertanejo').first()
    
    subgenres_data = [
        {
            'name': 'Forró Pé de Serra',
            'slug': 'forro-pe-de-serra',
            'parent': forro,
            'description': 'Forró tradicional nordestino',
            'color': '#FF8E8E'
        },
        {
            'name': 'Forró Universitário',
            'slug': 'forro-universitario',
            'parent': forro,
            'description': 'Forró moderno e universitário',
            'color': '#FFB3B3'
        },
        {
            'name': 'Sertanejo Raiz',
            'slug': 'sertanejo-raiz',
            'parent': sertanejo,
            'description': 'Sertanejo tradicional',
            'color': '#7EDDDD'
        },
        {
            'name': 'Sertanejo Universitário',
            'slug': 'sertanejo-universitario',
            'parent': sertanejo,
            'description': 'Sertanejo moderno',
            'color': '#A8E6E6'
        }
    ]
    
    for subgenre_data in subgenres_data:
        if subgenre_data['parent']:
            subgenre, created = Genre.objects.get_or_create(
                slug=subgenre_data['slug'],
                defaults=subgenre_data
            )
            
            if created:
                print(f"✅ Subgênero criado: {subgenre.name} (filho de {subgenre.parent.name})")
            else:
                print(f"🔄 Subgênero já existe: {subgenre.name}")

if __name__ == '__main__':
    try:
        create_genres()
        create_subgenres()
        print("\n🎉 Gêneros criados com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao criar gêneros: {e}")
        sys.exit(1)
