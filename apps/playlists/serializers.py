from rest_framework import serializers
from .models import Playlist
from apps.music.serializers import MusicSerializer


class PlaylistSerializer(serializers.ModelSerializer):
    """Serializer para o modelo PlayHit"""
    
    musics_count = serializers.SerializerMethodField()
    musics_data = serializers.SerializerMethodField()
    
    class Meta:
        model = Playlist
        fields = [
            'id', 'name', 'cover', 'musics_count', 'musics_data',
            'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_musics_count(self, obj):
        """Retorna quantidade de músicas"""
        return obj.get_musics_count()
    
    def get_musics_data(self, obj):
        """Retorna dados completos das músicas"""
        musics = obj.musics.all()
        return MusicSerializer(musics, many=True, context=self.context).data


class PlaylistCreateSerializer(serializers.ModelSerializer):
    """Serializer para criação de PlayHit"""
    
    class Meta:
        model = Playlist
        fields = ['name', 'cover', 'is_active']
    
    def create(self, validated_data):
        """Cria uma nova playlist"""
        return super().create(validated_data)
    
    def validate_name(self, value):
        """Validação do nome"""
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Nome deve ter pelo menos 2 caracteres.")
        return value.strip()


class PlaylistDetailSerializer(serializers.ModelSerializer):
    """Serializer detalhado para PlayHit"""
    
    musics_count = serializers.SerializerMethodField()
    musics_data = serializers.SerializerMethodField()
    
    class Meta:
        model = Playlist
        fields = [
            'id', 'name', 'cover', 'musics',
            'musics_data', 'musics_count',
            'created_at', 'updated_at', 'is_active'
        ]
    
    def get_musics_count(self, obj):
        return obj.get_musics_count()
    
    def get_musics_data(self, obj):
        """Retorna dados completos das músicas"""
        musics = obj.musics.all()
        return MusicSerializer(musics, many=True, context=self.context).data


