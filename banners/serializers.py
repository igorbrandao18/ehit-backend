from rest_framework import serializers
from .models import Banner


class BannerSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Banner"""
    
    class Meta:
        model = Banner
        fields = [
            'id',
            'name',
            'image',
            'link',
            'start_date',
            'end_date',
            'is_active',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def to_representation(self, instance):
        """Customiza a representação do serializer"""
        data = super().to_representation(instance)
        
        # Verificar se o banner está ativo no momento
        data['is_active'] = instance.is_currently_active()
        
        return data

