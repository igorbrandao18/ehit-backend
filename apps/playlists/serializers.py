from rest_framework import serializers
from .models import Playlist, PlaylistMusic, UserFavorite


class PlaylistSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Playlist"""
    
    user_username = serializers.CharField(source='user.username', read_only=True)
    musics_count = serializers.SerializerMethodField()
    total_duration = serializers.SerializerMethodField()
    total_duration_formatted = serializers.CharField(source='get_total_duration_formatted', read_only=True)
    
    class Meta:
        model = Playlist
        fields = [
            'id', 'user', 'user_username', 'name', 'description',
            'is_public', 'cover', 'followers_count', 'musics_count',
            'total_duration', 'total_duration_formatted',
            'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'followers_count']
    
    def get_musics_count(self, obj):
        """Retorna quantidade de músicas"""
        return obj.get_musics_count()
    
    def get_total_duration(self, obj):
        """Retorna duração total"""
        return obj.get_total_duration()


class PlaylistCreateSerializer(serializers.ModelSerializer):
    """Serializer para criação de playlist"""
    
    class Meta:
        model = Playlist
        fields = [
            'name', 'description', 'is_public', 'cover'
        ]
    
    def validate_name(self, value):
        """Validação do nome"""
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Nome deve ter pelo menos 2 caracteres.")
        return value.strip()


class PlaylistMusicSerializer(serializers.ModelSerializer):
    """Serializer para PlaylistMusic"""
    
    music_title = serializers.CharField(source='music.title', read_only=True)
    music_artist = serializers.CharField(source='music.artist.stage_name', read_only=True)
    music_duration = serializers.IntegerField(source='music.duration', read_only=True)
    music_duration_formatted = serializers.CharField(source='music.get_duration_formatted', read_only=True)
    
    class Meta:
        model = PlaylistMusic
        fields = [
            'id', 'playlist', 'music', 'music_title', 'music_artist',
            'music_duration', 'music_duration_formatted', 'order', 'added_at'
        ]
        read_only_fields = ['id', 'added_at']


class PlaylistDetailSerializer(serializers.ModelSerializer):
    """Serializer detalhado para playlist"""
    
    user_username = serializers.CharField(source='user.username', read_only=True)
    musics = PlaylistMusicSerializer(source='playlistmusic_set', many=True, read_only=True)
    musics_count = serializers.SerializerMethodField()
    total_duration_formatted = serializers.CharField(source='get_total_duration_formatted', read_only=True)
    
    class Meta:
        model = Playlist
        fields = [
            'id', 'user', 'user_username', 'name', 'description',
            'is_public', 'cover', 'followers_count', 'musics',
            'musics_count', 'total_duration_formatted',
            'created_at', 'updated_at', 'is_active'
        ]
    
    def get_musics_count(self, obj):
        return obj.get_musics_count()


class UserFavoriteSerializer(serializers.ModelSerializer):
    """Serializer para UserFavorite"""
    
    music_title = serializers.CharField(source='music.title', read_only=True)
    music_artist = serializers.CharField(source='music.artist.stage_name', read_only=True)
    music_genre = serializers.CharField(source='music.genre', read_only=True)
    music_duration_formatted = serializers.CharField(source='music.get_duration_formatted', read_only=True)
    music_cover = serializers.ImageField(source='music.cover', read_only=True)
    
    class Meta:
        model = UserFavorite
        fields = [
            'id', 'music', 'music_title', 'music_artist', 'music_genre',
            'music_duration_formatted', 'music_cover', 'added_at'
        ]
        read_only_fields = ['id', 'added_at']


class UserFavoriteCreateSerializer(serializers.ModelSerializer):
    """Serializer para criação de favorito"""
    
    class Meta:
        model = UserFavorite
        fields = ['music']
    
    def validate(self, attrs):
        """Validação de favorito único"""
        user = self.context['request'].user
        music = attrs['music']
        
        if UserFavorite.objects.filter(user=user, music=music).exists():
            raise serializers.ValidationError("Esta música já está nos seus favoritos.")
        
        return attrs
