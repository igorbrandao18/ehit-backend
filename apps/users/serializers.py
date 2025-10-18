from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer para o modelo User"""
    
    user_type_display = serializers.CharField(source='get_user_type_display', read_only=True)
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'full_name',
            'user_type', 'user_type_display', 'bio', 'avatar', 'phone',
            'birth_date', 'location', 'verified', 'followers_count',
            'date_joined', 'is_active'
        ]
        read_only_fields = ['id', 'date_joined', 'followers_count']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def get_full_name(self, obj):
        """Retorna nome completo"""
        return f"{obj.first_name} {obj.last_name}".strip()
    
    def create(self, validated_data):
        """Cria usuário com senha criptografada"""
        password = validated_data.pop('password', None)
        user = User.objects.create(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user
    
    def update(self, instance, validated_data):
        """Atualiza usuário"""
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer para criação de usuário"""
    
    password = serializers.CharField(write_only=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'user_type', 'bio',
            'phone', 'birth_date', 'location'
        ]
    
    def validate(self, attrs):
        """Validação de senhas"""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("As senhas não coincidem.")
        return attrs
    
    def create(self, validated_data):
        """Cria usuário"""
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer para perfil do usuário"""
    
    user_type_display = serializers.CharField(source='get_user_type_display', read_only=True)
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'full_name',
            'user_type', 'user_type_display', 'bio', 'avatar', 'phone',
            'birth_date', 'location', 'verified', 'followers_count',
            'date_joined'
        ]
        read_only_fields = ['id', 'username', 'date_joined', 'followers_count', 'verified']
    
    def get_full_name(self, obj):
        """Retorna nome completo"""
        return f"{obj.first_name} {obj.last_name}".strip()
