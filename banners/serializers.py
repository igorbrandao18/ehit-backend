from rest_framework import serializers
from .models import Banner


class BannerSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Banner"""
    
    is_currently_active = serializers.SerializerMethodField()
    
    class Meta:
        model = Banner
        fields = [
            'id',
            'name',
            'image',
            'link',
            'start_date',
            'end_date',
            'is_currently_active',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_is_currently_active(self, obj):
        """Retorna se o banner está ativo no momento"""
        return obj.is_currently_active()
    
    def to_representation(self, instance):
        """Customiza a representação do serializer"""
        return super().to_representation(instance)

