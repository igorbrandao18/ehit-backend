from rest_framework import serializers
from .models import Artist, Album


class GenreSerializer(serializers.ModelSerializer):
    """Serializer simplificado para gênero"""
    class Meta:
        model = Artist.genre.field.related_model
        fields = ['id', 'name', 'slug', 'color', 'icon']


class AlbumSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Album com músicas"""
    
    artist_name = serializers.CharField(source='artist.stage_name', read_only=True)
    musics_count = serializers.SerializerMethodField()
    musics = serializers.SerializerMethodField()
    
    class Meta:
        model = Album
        fields = [
            'id', 'artist', 'artist_name', 'name', 'cover', 
            'release_date', 'featured', 'musics_count', 'musics',
            'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_musics_count(self, obj):
        """Retorna quantidade de músicas no álbum"""
        return obj.get_musics_count()
    
    def get_musics(self, obj):
        """Retorna as músicas do álbum"""
        from apps.music.serializers import MusicSerializer
        musics = obj.musics.filter(is_active=True).order_by('-created_at')
        return MusicSerializer(musics, many=True, context=self.context).data
    
    def to_representation(self, instance):
        """Gera URL absoluta para cover (padrão playlists)."""
        data = super().to_representation(instance)
        request = self.context.get('request') if hasattr(self, 'context') else None
        cover_field = getattr(instance, 'cover', None)
        if cover_field and getattr(cover_field, 'url', None):
            url = cover_field.url
            data['cover'] = request.build_absolute_uri(url) if request else url
        return data


class AlbumCreateSerializer(serializers.ModelSerializer):
    """Serializer para criação de álbum"""
    
    class Meta:
        model = Album
        fields = ['artist', 'name', 'cover', 'release_date', 'featured', 'is_active']
    
    def validate_name(self, value):
        """Validação do nome do álbum"""
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Nome do álbum deve ter pelo menos 2 caracteres.")
        return value.strip()


class ArtistSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Artist simplificado"""
    
    genre_data = GenreSerializer(source='genre', read_only=True)
    albums_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Artist
        fields = [
            'id', 'stage_name', 'photo', 'genre', 'genre_data', 'albums_count',
            'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_albums_count(self, obj):
        """Retorna quantidade de álbuns do artista"""
        return obj.albums.count()


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
