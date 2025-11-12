from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Role
from django.db import transaction

import logging
logger = logging.getLogger(__name__)


class RegisterSerializer(serializers.Serializer):
    """
    Serializador para el REGISTRO de un nuevo usuario.
    Toma los 3 campos del frontend: Nombre, Correo, Contraseña.
    """
    full_name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8, error_messages={
        "min_length": "La contraseña debe tener al menos 8 caracteres."
    })

    def validate_email(self, value):
        """Verifica si el email ya existe (el 'username' es el email)"""
        # Pasamos el email a minúsculas para evitar duplicados
        normalized_email = value.lower()
        if User.objects.filter(username=normalized_email).exists():
            raise serializers.ValidationError("Este correo electrónico ya está registrado.")
        return normalized_email 

    @transaction.atomic # Asegura que todo se cree junto, o nada
    def create(self, validated_data):
        logger.info("Iniciando creación de usuario...")
        
        # 1. Obtenemos el rol "Cliente". Si no existe, lo creamos.
        # (En producción, esto se debe crear desde el admin)
        try:
            client_role, created = Role.objects.get_or_create(name="Cliente")
            if created:
                logger.warning("Rol 'Cliente' no existía, fue creado.")
        except Exception as e:
            logger.error(f"Error al obtener/crear rol 'Cliente': {e}")
            raise serializers.ValidationError("Error interno al configurar el rol de usuario.")

        # 2. Creamos el 'auth_user'
        # Usamos el email como 'username' para el login
        try:
            user = User.objects.create_user(
                username=validated_data['email'], # email en minúsculas
                email=validated_data['email'],
                password=validated_data['password']
            )
            # Guardamos el nombre en el 'auth_user' también, es útil
            user.first_name = validated_data['full_name']
            user.save()
            logger.info(f"Usuario 'auth_user' creado: {user.username}")
        except Exception as e:
            logger.error(f"Error al crear 'auth_user': {e}")
            raise serializers.ValidationError("Error interno al crear el usuario.")

        # 3. Creamos el 'UserProfile' (el "corazón")
        # ¡Nuestro signal 'create_user_wallet' se disparará automáticamente después de esto!
        try:
            profile = UserProfile.objects.create(
                user=user,
                full_name=validated_data['full_name'],
                phone="" # El teléfono se pedirá después al "Editar Perfil"
            )
            logger.info(f"Perfil 'UserProfile' creado para: {user.username}")
        except Exception as e:
            logger.error(f"Error al crear 'UserProfile': {e}")
            # Si esto falla, la transacción (atomic) revertirá la creación del 'auth_user'
            raise serializers.ValidationError("Error interno al crear el perfil de usuario.")

        # 4. Asignamos el rol de "Cliente"
        profile.roles.add(client_role)
        
        return user
    
# ---------------------------------------------------------------------------
# ¡¡¡CÓDIGO NUEVO!!! (Paso 13)
# VISTA 2: VER Y EDITAR PERFIL
# ---------------------------------------------------------------------------
class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializador para MOSTRAR y ACTUALIZAR el perfil del usuario.
    """
    # Traemos el 'email' del modelo User (auth_user)
    email = serializers.EmailField(source='user.email')

    class Meta:
        model = UserProfile
        # Estos son los campos que la API mostrará y permitirá editar
        fields = (
            'full_name', 
            'phone', 
            'email',
            'average_rating', # Solo mostramos el rating, no lo dejamos editar
            'total_ratings',
        )
        # Hacemos que los ratings sean "solo lectura"
        read_only_fields = ('average_rating', 'total_ratings')

    @transaction.atomic
    def update(self, instance, validated_data):
        # 'instance' es el UserProfile que estamos actualizando.
        
        # 1. Sacamos los datos del 'user' (email) si es que vienen
        user_data = validated_data.pop('user', {})
        new_email = user_data.get('email')

        # 2. Actualizamos el 'UserProfile' (full_name, phone)
        # Esto es lo normal:
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.save()

        # 3. Actualizamos el 'User' (email) si cambió
        if new_email and instance.user.email != new_email:
            # Verificamos que el nuevo email no esté ya en uso
            normalized_email = new_email.lower()
            if User.objects.filter(username=normalized_email).exclude(pk=instance.user.pk).exists():
                raise serializers.ValidationError({"email": "Este correo electrónico ya está en uso."})
            
            instance.user.email = normalized_email
            instance.user.username = normalized_email # ¡Actualizamos el username también!
            instance.user.save()

        return instance
    
# ¡¡¡CÓDIGO NUEVO!!! (Paso 14)
# VISTA 3: CAMBIAR CONTRASEÑA
# ---------------------------------------------------------------------------
class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializador para la pantalla de "Cambiar Contraseña".
    Toma 3 campos: contraseña antigua y la nueva (con confirmación).
    """
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True, min_length=8)
    new_password_confirm = serializers.CharField(required=True, write_only=True)

    def validate_old_password(self, value):
        """
        Verifica que la 'contraseña actual' (old_password) sea correcta.
        """
        # self.context['request'] nos da el usuario que está logueado (el del "Pase VIP")
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("La contraseña actual no es correcta.")
        return value

    def validate(self, data):
        """
        Verifica que las dos contraseñas nuevas (new_password y new_password_confirm)
        sean idénticas.
        """
        if data['new_password'] != data['new_password_confirm']:
            raise serializers.ValidationError({"new_password_confirm": "Las contraseñas nuevas no coinciden."})
        return data

    def save(self, **kwargs):
        """
        Guarda la nueva contraseña.
        """
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user