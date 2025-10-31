from rest_framework import serializers
from .models import Music


class GenreSerializer(serializers.ModelSerializer):
    """Serializer simplificado para gênero"""
    name = serializers.CharField(allow_null=True, default=None)
    slug = serializers.CharField(allow_null=True, default=None)
    color = serializers.CharField(allow_null=True, default=None)
    icon = serializers.CharField(allow_null=True, default=None)
    
    class Meta:
        model = Music.genre.field.related_model
        fields = ['id', 'name', 'slug', 'color', 'icon']


class AlbumSerializer(serializers.ModelSerializer):
    """Serializer simplificado para álbum"""
    name = serializers.CharField(allow_null=True, default=None)
    cover = serializers.ImageField(allow_null=True, read_only=True)
    featured = serializers.BooleanField(allow_null=True, default=False)
    
    class Meta:
        model = Music.album.field.related_model
        fields = ['id', 'name', 'cover', 'featured']


class MusicSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Music"""
    
    artist_name = serializers.CharField(source='artist.stage_name', read_only=True, allow_null=True)
    album_name = serializers.CharField(source='album.name', read_only=True, allow_null=True, default=None)
    album_featured = serializers.BooleanField(source='album.featured', read_only=True, allow_null=True, default=False)
    genre_data = GenreSerializer(source='genre', read_only=True, allow_null=True)
    album_data = AlbumSerializer(source='album', read_only=True, allow_null=True)
    stream_url = serializers.CharField(source='get_stream_url', read_only=True, allow_null=True)
    download_url = serializers.CharField(source='get_download_url', read_only=True, allow_null=True)
    file_size_mb = serializers.SerializerMethodField()
    is_popular = serializers.BooleanField(read_only=True, default=False)
    is_trending = serializers.BooleanField(read_only=True, default=False)
    
    class Meta:
        model = Music
        fields = [
            'id', 'artist', 'artist_name', 'album', 'album_name', 'album_featured', 'album_data',
            'title', 'genre', 'genre_data', 'duration', 'file', 'file_size_mb',
            'cover', 'release_date', 'streams_count', 'downloads_count', 'likes_count',
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
    
    def get_file_size_mb(self, obj):
        """Retorna o tamanho do arquivo em MB"""
        return obj.get_file_size_mb()
    
    def to_representation(self, instance):
        """Gera URLs absolutas para file e cover (padrão playlists)."""
        data = super().to_representation(instance)
        request = self.context.get('request') if hasattr(self, 'context') else None
        # Absolutizar file
        file_field = getattr(instance, 'file', None)
        if file_field and getattr(file_field, 'url', None):
            url = file_field.url
            data['file'] = request.build_absolute_uri(url) if request else url
        # Absolutizar cover
        cover_field = getattr(instance, 'cover', None)
        if cover_field and getattr(cover_field, 'url', None):
            url = cover_field.url
            data['cover'] = request.build_absolute_uri(url) if request else url
        return data


class MusicCreateSerializer(serializers.ModelSerializer):
    """Serializer para criação de música"""
    
    class Meta:
        model = Music
        fields = [
            'artist', 'album', 'title', 'genre', 'duration',
            'file', 'cover', 'release_date', 'is_featured'
        ]
        extra_kwargs = {
            'file': {'required': False, 'allow_null': True}
        }
    
    def validate_title(self, value):
        """Validação do título"""
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Título deve ter pelo menos 2 caracteres.")
        return value.strip()


class MusicStatsSerializer(serializers.ModelSerializer):
    """Serializer para estatísticas da música"""
    
    artist_name = serializers.CharField(source='artist.stage_name', read_only=True)
    album_name = serializers.CharField(source='album.name', read_only=True)
    
    class Meta:
        model = Music
        fields = [
            'id', 'title', 'artist_name', 'album_name', 'streams_count',
            'downloads_count', 'likes_count'
        ]


class MusicAutocompleteSerializer(serializers.ModelSerializer):
    """Serializer otimizado para autocomplete de músicas"""
    
    artist_name = serializers.CharField(source='artist.stage_name', read_only=True)
    album_name = serializers.CharField(source='album.name', read_only=True)
    
    class Meta:
        model = Music
        fields = [
            'id', 'title', 'artist_name', 'album_name', 'genre',
            'cover'
        ]


class MusicTrendingSerializer(serializers.ModelSerializer):
    """Serializer para músicas trending"""
    
    artist_name = serializers.CharField(source='artist.stage_name', read_only=True)
    album_name = serializers.CharField(source='album.name', read_only=True)
    
    class Meta:
        model = Music
        fields = [
            'id', 'title', 'artist_name', 'album_name', 'genre',
            'streams_count', 'likes_count',
            'is_featured', 'cover'
        ]
