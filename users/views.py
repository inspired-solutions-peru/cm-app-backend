from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .serializers import RegisterSerializer, UserProfileSerializer, ChangePasswordSerializer
from .models import UserProfile

import logging
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# VISTA 1: REGISTRO (Mejorada con Vistas Genéricas)
# /api/users/register/
# ---------------------------------------------------------------------------
class RegisterView(generics.CreateAPIView):
    """
    Vista para crear un nuevo usuario (Registro).
    Solo permite peticiones POST.
    """
    permission_classes = (permissions.AllowAny,) # Cualquiera puede registrarse
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = serializer.save()
            logger.info(f"Usuario creado exitosamente: {user.username}")
            return Response(
                {"message": "¡Usuario creado con éxito!"},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            logger.error(f"Error inesperado durante el registro: {e}")
            return Response(
                {"error": "Ocurrió un error inesperado durante el registro."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# ---------------------------------------------------------------------------
# ¡¡¡CÓDIGO NUEVO!!! (Paso 13.2)
# VISTA 2: VER Y EDITAR PERFIL
# /api/users/profile/
# ---------------------------------------------------------------------------
class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    Vista para ver (GET) y actualizar (PUT/PATCH) el perfil
    del usuario que está actualmente logueado.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated] # ¡PROTEGIDA!

    def get_object(self):
        """
        Sobrescribimos este método para que siempre devuelva
        el perfil del usuario que está haciendo la petición (el del "Pase VIP").
        """
        try:
            # request.user nos lo da el "Pase VIP" (JWT)
            return self.request.user.profile
        except UserProfile.DoesNotExist:
            logger.error(f"Error crítico: El usuario {self.request.user.username} no tiene UserProfile.")
            # Esto no debería pasar gracias a nuestros signals, pero es bueno tenerlo.
            return None 

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is None:
            return Response(
                {"error": "Perfil de usuario no encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if instance is None:
            return Response(
                {"error": "Perfil de usuario no encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        try:
            self.perform_update(serializer)
            logger.info(f"Perfil actualizado para: {request.user.username}")
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error al actualizar perfil para {request.user.username}: {e}")
            return Response(
                {"error": "Ocurrió un error al actualizar el perfil."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
# ¡¡¡CÓDIGO NUEVO!!! (Paso 14.2)
# VISTA 3: CAMBIAR CONTRASEÑA
# /api/users/change-password/
# ---------------------------------------------------------------------------
class ChangePasswordView(generics.UpdateAPIView):
    """
    Vista para cambiar la contraseña del usuario logueado.
    Solo permite peticiones PUT (para actualizar).
    """
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated] # ¡PROTEGIDA!

    def get_object(self):
        # El objeto que estamos actualizando es el 'auth_user'
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        # Pasamos el 'context' para que el serializer pueda acceder al request.user
        # y verificar la 'old_password'
        serializer = self.get_serializer(user, data=request.data, context={'request': request})
        
        serializer.is_valid(raise_exception=True)
        
        # El método .save() del serializer (que definimos) se encarga de cambiar la clave
        serializer.save()
        
        logger.info(f"Contraseña cambiada para: {user.username}")
        return Response(
            {"message": "Contraseña actualizada con éxito."},
            status=status.HTTP_200_OK
        )