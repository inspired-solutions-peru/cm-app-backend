from django.urls import path
# ¡Importamos la nueva vista!
from .views import RegisterView, UserProfileView, ChangePasswordView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # --- Endpoint de Registro (Ya lo tenías) ---
    # POST /api/users/register/
    path('register/', RegisterView.as_view(), name='register'),
    
    # --- Endpoints de Login (JWT) (Ya los tenías) ---
    # POST /api/users/token/
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # POST /api/users/token/refresh/
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # -----------------------------------------------------------------
    # ¡¡¡LÍNEA NUEVA!!! (Paso 13.3)
    # 3. Endpoint de Perfil (Ver y Editar)
    # -----------------------------------------------------------------
    # GET, PUT, PATCH /api/users/profile/
    path('profile/', UserProfileView.as_view(), name='user-profile'),

    # ¡¡¡LÍNEA NUEVA!!! (Paso 14.3)
    # 4. Endpoint de Cambiar Contraseña
    # -----------------------------------------------------------------
    # PUT /api/users/change-password/
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
]