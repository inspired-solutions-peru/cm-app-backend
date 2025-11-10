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
    # Django creará la tabla intermedia (users_userprofile_roles) por ti.
    roles = models.ManyToManyField(Role, related_name="users")

    # Campos de Ubicación (para la búsqueda inicial)
    # Usamos DecimalField para precisión.
    current_latitude = models.DecimalField(max_digits=22, decimal_places=16, null=True, blank=True)
    current_longitude = models.DecimalField(max_digits=22, decimal_places=16, null=True, blank=True)
    is_active_for_service = models.BooleanField(default=False, verbose_name="¿Activo para servicio?") # Ej. Conductor "en línea"

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    average_rating = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        default=5.00, 
        verbose_name="Calificación Promedio"
    )
    total_ratings = models.PositiveIntegerField(default=0, verbose_name="Total de Calificaciones")


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


class UserSavedLocation(models.Model):
    # Un perfil de usuario puede tener MUCHAS ubicaciones guardadas
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="saved_locations")

    name = models.CharField(max_length=100, verbose_name="Nombre del Lugar (ej. Casa)")
    address = models.CharField(max_length=255, verbose_name="Dirección")

    # Guardamos las coordenadas para no tener que buscarlas de nuevo
    latitude = models.DecimalField(max_digits=22, decimal_places=16)
    longitude = models.DecimalField(max_digits=22, decimal_places=16)

    # (Opcional) Podemos añadir un ícono, como en el frontend
    icon_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Nombre del Ícono (ej. 'home', 'work')")

    def __str__(self):
        return f"{self.user_profile.full_name} - {self.name} ({self.address})"

    class Meta:
        verbose_name = "Ubicación Guardada"
        verbose_name_plural = "Ubicaciones Guardadas"

# MODELO 6: TIPO DE MÉTODO DE PAGO
# (Catálogo: Tarjeta, Yape, Plin, Efectivo)
# ---------------------------------------------------------------------------
class PaymentMethodType(models.Model):
    class Types(models.TextChoices):
        TARJETA = 'TARJETA', 'Tarjeta'
        YAPE = 'YAPE', 'Yape'
        PLIN = 'PLIN', 'Plin'
        EFECTIVO = 'EFECTIVO', 'Efectivo'

    name = models.CharField(
        max_length=20,
        choices=Types.choices,
        unique=True,
        verbose_name="Nombre del Método"
    )
    icon_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Nombre del Ícono")

    def __str__(self):
        return self.get_name_display() # Muestra el valor legible (ej. "Tarjeta")

    class Meta:
        verbose_name = "Tipo de Método de Pago"
        verbose_name_plural = "Tipos de Métodos de Pago"

# ---------------------------------------------------------------------------
# ¡¡¡CÓDIGO NUEVO!!! (Paso 2)
# MODELO 7: MÉTODO DE PAGO DEL USUARIO
# (La tarjeta Visa 1234 o el Yape de un usuario específico)
# ---------------------------------------------------------------------------
class UserPaymentMethod(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="payment_methods")
    payment_type = models.ForeignKey(PaymentMethodType, on_delete=models.PROTECT, related_name="user_methods")

    # Un nombre amigable que el usuario puede poner
    nickname = models.CharField(max_length=50, blank=True, null=True, verbose_name="Apodo (ej. Visa Personal)")

    # Campos específicos para TARJETAS (pueden ser nulos para Yape/Plin/Efectivo)
    card_brand = models.CharField(max_length=50, blank=True, null=True, verbose_name="Marca (Visa, Mastercard)")
    last_four_digits = models.CharField(max_length=4, blank=True, null=True, verbose_name="Últimos 4 dígitos")
    # NO GUARDAMOS EL NÚMERO COMPLETO NI EL CVV, ¡NUNCA!
    # En una app real, aquí guardarías un 'payment_token' de un procesador de pagos (Stripe, Culqi, etc.)
    payment_token = models.CharField(max_length=255, blank=True, null=True, verbose_name="Token de Pago")
    
    # Campo para Yape/Plin (ej. número de teléfono)
    identifier = models.CharField(max_length=100, blank=True, null=True, verbose_name="Identificador (ej. N° de Yape)")
    
    is_default = models.BooleanField(default=False, verbose_name="¿Es método por defecto?")

    def __str__(self):
        if self.payment_type.name == PaymentMethodType.Types.TARJETA:
            return f"{self.user_profile.full_name} - {self.card_brand} **** {self.last_four_digits}"
        else:
            return f"{self.user_profile.full_name} - {self.payment_type.get_name_display()}"

    class Meta:
        verbose_name = "Método de Pago de Usuario"
        verbose_name_plural = "Métodos de Pago de Usuarios"
        # Opcional: Un usuario no puede tener la misma tarjeta dos veces
        unique_together = ('user_profile', 'payment_token', 'last_four_digits') 