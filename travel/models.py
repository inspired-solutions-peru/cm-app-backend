from django.db import models
from users.models import UserProfile # <-- ¡Importamos el PERFIL de nuestra app 'usuarios'!

# Create your models here.

class Viaje(models.Model):
    # Definimos los "estados" que puede tener un viaje
    # Esto es más limpio que usar strings
    class EstadoViaje(models.TextChoices):
        BUSCANDO = 'BUSCANDO', 'Buscando Conductor'
        ACEPTADO = 'ACEPTADO', 'Conductor Aceptó'
        EN_CAMINO = 'EN_CAMINO', 'Conductor en Camino'
        EN_PROGRESO = 'EN_PROGRESO', 'Viaje en Progreso'
        FINALIZADO = 'FINALIZADO', 'Viaje Finalizado'
        CANCELADO = 'CANCELADO', 'Viaje Cancelado'

    # --- RELACIONES (QUIÉN) ---
    # Un UserProfile (Pasajero) puede tener muchos viajes
    pasajero = models.ForeignKey(
        UserProfile, 
        on_delete=models.SET_NULL, # Si el pasajero borra su cuenta, el viaje no se borra (por historial)
        null=True,
        related_name="viajes_como_pasajero"
    )
    # Un UserProfile (Conductor) puede tener muchos viajes
    conductor = models.ForeignKey(
        UserProfile, 
        on_delete=models.SET_NULL,
        null=True, # <-- ¡Importante! Es nulo al inicio, cuando el viaje se está "BUSCANDO"
        blank=True,
        related_name="viajes_como_conductor"
    )

    # --- ESTADO (QUÉ) ---
    estado = models.CharField(
        max_length=20,
        choices=EstadoViaje.choices,
        default=EstadoViaje.BUSCANDO, # Todo viaje empieza "BUSCANDO"
        verbose_name="Estado del Viaje"
    )

    # --- UBICACIÓN (DÓNDE) ---
    # Origen
    origen_lat = models.DecimalField(max_digits=22, decimal_places=16, verbose_name="Latitud Origen")
    origen_lng = models.DecimalField(max_digits=22, decimal_places=16, verbose_name="Longitud Origen")
    origen_direccion = models.CharField(max_length=255, blank=True, verbose_name="Dirección Origen")

    # Destino
    destino_lat = models.DecimalField(max_digits=22, decimal_places=16, verbose_name="Latitud Destino")
    destino_lng = models.DecimalField(max_digits=22, decimal_places=16, verbose_name="Longitud Destino")
    destino_direccion = models.CharField(max_length=255, blank=True, verbose_name="Dirección Destino")

    # --- DINERO (CUÁNTO) ---
    precio_estimado = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Precio Estimado")
    precio_final = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Precio Final")

    # --- TIEMPO (CUÁNDO) ---
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")

    def __str__(self):
        # Esto es para que se vea bonito en el Admin
        return f"Viaje #{self.id} - {self.pasajero.full_name} ({self.get_estado_display()})"

    class Meta:
        verbose_name = "Viaje"
        verbose_name_plural = "Viajes"
        ordering = ['-created_at'] # Los viajes más nuevos primero