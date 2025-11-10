from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import UserProfile  # Importamos el Perfil
from travel.models import Viaje       # Importamos el Viaje

# Create your models here.

class Review(models.Model):
    # --- RELACIONES ---
    # Quién escribió la reseña (ej. el Pasajero)
    reviewer_profile = models.ForeignKey(
        UserProfile, 
        on_delete=models.SET_NULL,
        null=True,
        related_name="reviews_given", # Reseñas que he dado
        verbose_name="Perfil del Reseñador"
    )
    
    # Sobre quién es la reseña (ej. el Conductor)
    reviewed_profile = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE, # Si se borra el perfil, se borran sus reseñas
        related_name="reviews_received", # Reseñas que he recibido
        verbose_name="Perfil del Reseñado"
    )
    
    # A qué viaje (o pedido) pertenece esta reseña
    # Usamos SET_NULL para que si se borra el viaje, la reseña no se pierda
    viaje = models.ForeignKey(
        Viaje,
        on_delete=models.SET_NULL,
        null=True,
        blank=True, # Puede ser nulo (ej. una reseña general de la app)
        related_name="reviews",
        verbose_name="Viaje Asociado"
    )
    # En el futuro, aquí puedes añadir:
    # pedido = models.ForeignKey(Pedido, ...)
    
    # --- DATOS DE LA RESEÑA ---
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], # Validamos que sea de 1 a 5
        verbose_name="Calificación (Estrellas)"
    )
    comment = models.TextField(blank=True, null=True, verbose_name="Comentario")
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reseña de {self.reviewer_profile.full_name} a {self.reviewed_profile.full_name} ({self.rating} estrellas)"

    class Meta:
        verbose_name = "Reseña y Calificación"
        verbose_name_plural = "Reseñas y Calificaciones"
        ordering = ['-created_at'] # Las más nuevas primero