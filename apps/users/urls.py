from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # Lista e criação de usuários
    path('', views.UserListView.as_view(), name='user-list'),
    path('create/', views.UserCreateView.as_view(), name='user-create'),
    path('<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
    path('me/', views.UserDetailView.as_view(), name='user-me'),
    
    # Autenticação
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/update/', views.update_profile_view, name='profile-update'),
    path('change-password/', views.change_password_view, name='change-password'),
    path('stats/', views.user_stats_view, name='user-stats'),
]
