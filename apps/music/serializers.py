from rest_framework import serializers
from .models import Music


class GenreSerializer(serializers.ModelSerializer):
    """Serializer simplificado para gênero"""
    class Meta:
        model = Music.genre.field.related_model
        fields = ['id', 'name', 'slug', 'color', 'icon']


class MusicSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Music"""
    
    artist_name = serializers.CharField(source='artist.stage_name', read_only=True)
    artist_username = serializers.CharField(source='artist.user.username', read_only=True)
    genre_data = GenreSerializer(source='genre', read_only=True)
    duration_formatted = serializers.CharField(source='get_duration_formatted', read_only=True)
    stream_url = serializers.CharField(source='get_stream_url', read_only=True)
    download_url = serializers.CharField(source='get_download_url', read_only=True)
    is_popular = serializers.BooleanField(read_only=True)
    is_trending = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Music
        fields = [
            'id', 'artist', 'artist_name', 'artist_username', 'title', 'album',
            'genre', 'genre_data', 'duration', 'duration_formatted', 'file', 'cover', 'lyrics',
            'release_date', 'streams_count', 'downloads_count', 'likes_count',
            'is_featured', 'is_popular', 'is_trending', 'stream_url',
            'download_url', 'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = [
            'id', 'created_at', 'updated_at', 'streams_count',
            'downloads_count', 'likes_count'
        ]
    
    def validate_title(self, value):
        """Validação do título"""
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Título deve ter pelo menos 2 caracteres.")
        return value.strip()
    
    def validate_duration(self, value):
        """Validação da duração"""
        if value <= 0:
            raise serializers.ValidationError("Duração deve ser maior que zero.")
        if value > 3600:  # 1 hora
            raise serializers.ValidationError("Duração não pode ser maior que 1 hora.")
        return value


class MusicCreateSerializer(serializers.ModelSerializer):
    """Serializer para criação de música"""
    
    class Meta:
        model = Music
        fields = [
            'title', 'album', 'genre', 'duration',
            'file', 'cover', 'lyrics', 'release_date'
        ]
    
    def create(self, validated_data):
        """Cria uma nova música associada ao artista atual"""
        user = self.context['request'].user
        # Assumir que o usuário é um artista
        from apps.artists.models import Artist
        try:
            artist = Artist.objects.get(user=user)
            validated_data['artist'] = artist
        except Artist.DoesNotExist:
            raise serializers.ValidationError("Usuário deve ser um artista para criar músicas.")
        return super().create(validated_data)
    
    def validate_title(self, value):
        """Validação do título"""
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Título deve ter pelo menos 2 caracteres.")
        return value.strip()


class MusicStatsSerializer(serializers.ModelSerializer):
    """Serializer para estatísticas da música"""
    
    artist_name = serializers.CharField(source='artist.stage_name', read_only=True)
    duration_formatted = serializers.CharField(source='get_duration_formatted', read_only=True)
    
    class Meta:
        model = Music
        fields = [
            'id', 'title', 'artist_name', 'streams_count',
            'downloads_count', 'likes_count', 'duration_formatted'
        ]


class MusicAutocompleteSerializer(serializers.ModelSerializer):
    """Serializer otimizado para autocomplete de músicas"""
    
    artist_name = serializers.CharField(source='artist.stage_name', read_only=True)
    duration_formatted = serializers.CharField(source='get_duration_formatted', read_only=True)
    
    class Meta:
        model = Music
        fields = [
            'id', 'title', 'artist_name', 'album', 'genre',
            'duration_formatted', 'cover'
        ]


class MusicTrendingSerializer(serializers.ModelSerializer):
    """Serializer para músicas trending"""
    
    artist_name = serializers.CharField(source='artist.stage_name', read_only=True)
    artist_verified = serializers.BooleanField(source='artist.verified', read_only=True)
    duration_formatted = serializers.CharField(source='get_duration_formatted', read_only=True)
    
    class Meta:
        model = Music
        fields = [
            'id', 'title', 'artist_name', 'artist_verified', 'genre',
            'duration_formatted', 'streams_count', 'likes_count',
            'is_featured', 'cover'
        ]
