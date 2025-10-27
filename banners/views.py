from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Banner
from .serializers import BannerSerializer


class BannerViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para banners (somente leitura)
    
    Retorna banners ativos no momento atual
    """
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        """Retorna apenas banners ativos"""
        return Banner.get_active_banners()
    
    @action(detail=False, methods=['get'])
    def all(self, request):
        """
        Retorna todos os banners (ativos e inativos)
        
        GET /api/banners/all/
        """
        banners = Banner.objects.all()
        serializer = self.get_serializer(banners, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """
        Retorna apenas banners ativos no momento
        (igual ao list padrão)
        
        GET /api/banners/active/
        """
        banners = Banner.get_active_banners()
        serializer = self.get_serializer(banners, many=True)
        return Response(serializer.data)

