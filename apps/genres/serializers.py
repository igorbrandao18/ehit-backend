from rest_framework import serializers
from .models import Genre

class GenreSerializer(serializers.ModelSerializer):
    song_count = serializers.ReadOnlyField()
    artist_count = serializers.ReadOnlyField()
    subgenres = serializers.SerializerMethodField()
    
    class Meta:
        model = Genre
        fields = [
            'id', 'name', 'slug', 'description', 'color', 'icon',
            'parent', 'is_active', 'song_count', 'artist_count',
            'subgenres', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']
    
    def get_subgenres(self, obj):
        """Retorna os subgêneros se existirem"""
        subgenres = obj.subgenres.filter(is_active=True)
        return GenreSerializer(subgenres, many=True).data

class GenreListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listagem"""
    song_count = serializers.ReadOnlyField()
    artist_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Genre
        fields = ['id', 'name', 'slug', 'color', 'icon', 'song_count', 'artist_count']
