from django.db import models
from django.conf import settings
from users.models import UserProfile # Importamos el Perfil
import uuid # Para códigos únicos

# Create your models here.

# ---------------------------------------------------------------------------
# MODELO 1: CUPÓN DE PROMOCIÓN (PROMO CODE)
# ---------------------------------------------------------------------------
class PromoCode(models.Model):

    class DiscountType(models.TextChoices):
        PERCENTAGE = 'PERCENTAGE', 'Porcentaje' # Ej. 10%
        FIXED = 'FIXED', 'Monto Fijo'           # Ej. S/ 5.00

    code = models.CharField(
        max_length=50, 
        unique=True, 
        verbose_name="Código del Cupón"
    )
    description = models.TextField(verbose_name="Descripción")
    
    discount_type = models.CharField(
        max_length=20,
        choices=DiscountType.choices,
        verbose_name="Tipo de Descuento"
    )
    discount_value = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name="Valor del Descuento"
    )
    max_discount_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        null=True, blank=True,
        verbose_name="Monto Máximo de Descuento (para porcentaje)"
    )
    
    valid_from = models.DateTimeField(verbose_name="Válido Desde")
    valid_to = models.DateTimeField(verbose_name="Válido Hasta")
    
    is_active = models.BooleanField(default=True, verbose_name="¿Está activo?")
    
    max_uses = models.PositiveIntegerField(default=1000, verbose_name="Usos Totales Máximos")
    uses_per_user = models.PositiveIntegerField(default=1, verbose_name="Usos por Usuario")
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.discount_type == self.DiscountType.PERCENTAGE:
            return f"{self.code} ({self.discount_value}%)"
        return f"{self.code} (S/ {self.discount_value})"

    class Meta:
        verbose_name = "Código de Promoción"
        verbose_name_plural = "Códigos de Promoción"

# ---------------------------------------------------------------------------
# MODELO 2: REGISTRO DE USO DE CUPONES
# ---------------------------------------------------------------------------
class UserPromoCodeUsage(models.Model):
    user_profile = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="promo_usages"
    )
    promo_code = models.ForeignKey(
        PromoCode,
        on_delete=models.CASCADE,
        related_name="usages"
    )
    used_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Uso")
    
    # (Opcional) Enlazar el uso a un viaje o pedido específico
    viaje = models.ForeignKey(
        'travel.Viaje', 
        on_delete=models.SET_NULL, 
        null=True, blank=True,
        related_name="promo_code_usage"
    )
    # pedido = models.ForeignKey('delivery.Pedido', ...)

    def __str__(self):
        return f"{self.user_profile.full_name} usó {self.promo_code.code}"

    class Meta:
        verbose_name = "Uso de Cupón"
        verbose_name_plural = "Usos de Cupones"
        # Un usuario solo puede usar el mismo cupón las veces que 'uses_per_user' diga
        # (Lógica más compleja se manejaría en la API)