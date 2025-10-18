from rest_framework import serializers
from .models import Artist


class ArtistSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Artist"""
    
    user_username = serializers.CharField(source='user.username', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    total_streams = serializers.SerializerMethodField()
    total_downloads = serializers.SerializerMethodField()
    total_likes = serializers.SerializerMethodField()
    
    class Meta:
        model = Artist
        fields = [
            'id', 'user', 'user_username', 'user_email', 'stage_name', 'real_name',
            'bio', 'genre', 'location', 'website', 'social_links',
            'verified', 'followers_count', 'monthly_listeners',
            'total_streams', 'total_downloads', 'total_likes',
            'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'followers_count', 'monthly_listeners']
    
    def get_total_streams(self, obj):
        """Retorna total de streams"""
        return obj.get_total_streams()
    
    def get_total_downloads(self, obj):
        """Retorna total de downloads"""
        return obj.get_total_downloads()
    
    def get_total_likes(self, obj):
        """Retorna total de curtidas"""
        return obj.get_total_likes()


class ArtistCreateSerializer(serializers.ModelSerializer):
    """Serializer para criação de artista"""
    
    class Meta:
        model = Artist
        fields = [
            'user', 'stage_name', 'real_name', 'bio', 'genre',
            'location', 'website', 'social_links'
        ]
    
    def validate_stage_name(self, value):
        """Validação do nome artístico"""
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Nome artístico deve ter pelo menos 2 caracteres.")
        return value.strip()


class ArtistStatsSerializer(serializers.ModelSerializer):
    """Serializer para estatísticas do artista"""
    
    total_streams = serializers.SerializerMethodField()
    total_downloads = serializers.SerializerMethodField()
    total_likes = serializers.SerializerMethodField()
    musics_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Artist
        fields = [
            'id', 'stage_name', 'followers_count', 'monthly_listeners',
            'total_streams', 'total_downloads', 'total_likes', 'musics_count'
        ]
    
    def get_total_streams(self, obj):
        return obj.get_total_streams()
    
    def get_total_downloads(self, obj):
        return obj.get_total_downloads()
    
    def get_total_likes(self, obj):
        return obj.get_total_likes()
    
    def get_musics_count(self, obj):
        return obj.musics.count()
