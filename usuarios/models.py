from django.db import models
from django.contrib.auth.models import User # El auth_user que ya existe
from django.conf import settings # Para usar el User

# Create your models here.

# ---------------------------------------------------------------------------
# MODELO 1: ROLES
# (Manager, Cliente, Conductor, Proveedor)
# ---------------------------------------------------------------------------
class Role(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Nombre del Rol")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Rol"
        verbose_name_plural = "Roles"


# ---------------------------------------------------------------------------
# MODELO 2: PERFIL DE USUARIO (EL PERFIL CENTRAL)
# (Este perfil es compartido por Clientes, Conductores, etc.)
# ---------------------------------------------------------------------------
class UserProfile(models.Model):
    # Usamos OneToOne porque un User (de auth_user) solo tiene UN perfil
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    
    # Datos obligatorios que pediste para el Cliente
    full_name = models.CharField(max_length=100, verbose_name="Nombre Completo")
    phone = models.CharField(max_length=20, unique=True, verbose_name="Teléfono")
    
    # La relación Muchos-a-Muchos que pediste.
    # Django creará la tabla intermedia (usuarios_userprofile_roles) por ti.
    roles = models.ManyToManyField(Role, related_name="users")

    # Campos de Ubicación (para la búsqueda inicial)
    # Usamos DecimalField para precisión.
    current_latitude = models.DecimalField(max_digits=22, decimal_places=16, null=True, blank=True)
    current_longitude = models.DecimalField(max_digits=22, decimal_places=16, null=True, blank=True)
    is_active_for_service = models.BooleanField(default=False, verbose_name="¿Activo para servicio?") # Ej. Conductor "en línea"

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Perfil de {self.user.username} ({self.full_name})"

    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuario"

# ---------------------------------------------------------------------------
# MODELO 3: DATOS DEL CONDUCTOR (CAMPOS OBLIGATORIOS)
# (Datos específicos que solo aplican al rol "Conductor")
# ---------------------------------------------------------------------------
class DriverData(models.Model):
    # Un perfil solo puede tener UNA data de conductor
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name="driver_data")

    # Campos obligatorios que pediste
    dni = models.CharField(max_length=20, unique=True, verbose_name="DNI")
    license_number = models.CharField(max_length=50, verbose_name="Número de Licencia")
    soat_number = models.CharField(max_length=100, verbose_name="SOAT")
    vehicle_plate = models.CharField(max_length=10, unique=True, verbose_name="Placa del Vehículo")
    vehicle_card = models.CharField(max_length=100, verbose_name="Tarjeta de Propiedad")

    # Campos opcionales
    vehicle_model = models.CharField(max_length=50, blank=True, null=True, verbose_name="Modelo del Vehículo")
    vehicle_color = models.CharField(max_length=30, blank=True, null=True, verbose_name="Color del Vehículo")

    is_verified = models.BooleanField(default=False, verbose_name="¿Datos Verificados?")

    def __str__(self):
        return f"Datos de Conductor para {self.user_profile.full_name} (Placa: {self.vehicle_plate})"

    class Meta:
        verbose_name = "Datos de Conductor"
        verbose_name_plural = "Datos de Conductores"

# ---------------------------------------------------------------------------
# MODELO 4: DATOS DEL PROVEEDOR (PARA DELIVERY Y SERVICIOS)
# (Ej. una tienda, un restaurante, un gasfitero)
# ---------------------------------------------------------------------------
class ProviderData(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name="provider_data")
    
    store_name = models.CharField(max_length=150, verbose_name="Nombre de Tienda/Negocio")
    store_address = models.CharField(max_length=255, verbose_name="Dirección")
    # RUC, etc.
    
    def __str__(self):
        return f"Datos de Proveedor: {self.store_name}"
    
    class Meta:
        verbose_name = "Datos de Proveedor"
        verbose_name_plural = "Datos de Proveedores"