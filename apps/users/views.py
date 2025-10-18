from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from .models import User
from .serializers import UserSerializer, UserCreateSerializer, UserProfileSerializer


class StandardResultsSetPagination(PageNumberPagination):
    """Paginação padrão"""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class UserListView(generics.ListAPIView):
    """Lista de usuários"""
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filtros de busca"""
        queryset = super().get_queryset()
        
        # Filtro por tipo de usuário
        user_type = self.request.query_params.get('user_type')
        if user_type:
            queryset = queryset.filter(user_type=user_type)
        
        # Filtro por verificação
        verified = self.request.query_params.get('verified')
        if verified is not None:
            queryset = queryset.filter(verified=verified.lower() == 'true')
        
        # Busca por nome/username
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(username__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search)
            )
        
        return queryset.order_by('-followers_count', '-date_joined')


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Detalhes do usuário"""
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        """Retorna usuário atual ou usuário específico"""
        if self.kwargs.get('pk') == 'me':
            return self.request.user
        return super().get_object()


class UserCreateView(generics.CreateAPIView):
    """Criação de usuário"""
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    """Login de usuário"""
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {'error': 'Username e password são obrigatórios'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = authenticate(username=username, password=password)
    
    if user and user.is_active:
        serializer = UserSerializer(user)
        return Response({
            'user': serializer.data,
            'message': 'Login realizado com sucesso'
        })
    else:
        return Response(
            {'error': 'Credenciais inválidas'},
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def profile_view(request):
    """Perfil do usuário logado"""
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data)


@api_view(['PUT', 'PATCH'])
@permission_classes([permissions.IsAuthenticated])
def update_profile_view(request):
    """Atualização do perfil"""
    serializer = UserProfileSerializer(
        request.user,
        data=request.data,
        partial=request.method == 'PATCH'
    )
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def change_password_view(request):
    """Alteração de senha"""
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')
    confirm_password = request.data.get('confirm_password')
    
    if not all([old_password, new_password, confirm_password]):
        return Response(
            {'error': 'Todos os campos são obrigatórios'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if new_password != confirm_password:
        return Response(
            {'error': 'Nova senha e confirmação não coincidem'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if len(new_password) < 6:
        return Response(
            {'error': 'Nova senha deve ter pelo menos 6 caracteres'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if not request.user.check_password(old_password):
        return Response(
            {'error': 'Senha atual incorreta'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    request.user.set_password(new_password)
    request.user.save()
    
    return Response({'message': 'Senha alterada com sucesso'})


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_stats_view(request):
    """Estatísticas do usuário"""
    user = request.user
    
    stats = {
        'followers_count': user.followers_count,
        'user_type': user.get_user_type_display(),
        'verified': user.verified,
        'date_joined': user.date_joined,
        'is_active': user.is_active
    }
    
    # Estatísticas específicas por tipo de usuário
    if user.is_artist and hasattr(user, 'artist_profile'):
        artist = user.artist_profile
        stats.update({
            'stage_name': artist.stage_name,
            'monthly_listeners': artist.monthly_listeners,
            'total_streams': artist.get_total_streams(),
            'total_downloads': artist.get_total_downloads(),
            'total_likes': artist.get_total_likes(),
            'musics_count': artist.musics.count()
        })
    
    return Response(stats)