from rest_framework import serializers
from .models import Artist


class GenreSerializer(serializers.ModelSerializer):
    """Serializer simplificado para gênero"""
    class Meta:
        model = Artist.genre.field.related_model
        fields = ['id', 'name', 'slug', 'color', 'icon']


class ArtistSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Artist simplificado"""
    
    genre_data = GenreSerializer(source='genre', read_only=True)
    
    class Meta:
        model = Artist
        fields = [
            'id', 'stage_name', 'photo', 'genre', 'genre_data',
            'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ArtistCreateSerializer(serializers.ModelSerializer):
    """Serializer para criação de artista"""
    
    class Meta:
        model = Artist
        fields = ['stage_name', 'photo', 'genre', 'is_active']
    
    def validate_stage_name(self, value):
        """Validação do nome artístico"""
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Nome artístico deve ter pelo menos 2 caracteres.")
        return value.strip()
