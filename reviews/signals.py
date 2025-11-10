from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg, Count
from .models import Review
from users.models import UserProfile

# Esta función calcula y actualiza el promedio del perfil reseñado
def update_profile_rating(profile_id):
    try:
        profile = UserProfile.objects.get(id=profile_id)
        
        # Obtenemos todas las reseñas para este perfil
        reviews = Review.objects.filter(reviewed_profile=profile)
        
        if reviews.exists():
            # Usamos la base de datos para calcular el promedio (Avg) y el conteo (Count)
            agg_data = reviews.aggregate(
                average_rating=Avg('rating'),
                total_ratings=Count('id')
            )
            
            # Actualizamos los campos del perfil
            profile.average_rating = agg_data['average_rating']
            profile.total_ratings = agg_data['total_ratings']
        else:
            # Si no hay reseñas, reseteamos a los valores por defecto
            profile.average_rating = 5.00
            profile.total_ratings = 0
            
        profile.save() # Guardamos el perfil con los nuevos valores

    except UserProfile.DoesNotExist:
        pass # El perfil no existe, no hacemos nada

# -------------------------------------------------------------------
# "SIGNAL" (El Gatillo)
# -------------------------------------------------------------------
# Esta función se "dispara" CADA VEZ que una 'Review' se guarda (post_save)
@receiver(post_save, sender=Review)
def review_saved_handler(sender, instance, created, **kwargs):
    # 'instance' es la Reseña que se acaba de guardar
    update_profile_rating(instance.reviewed_profile.id)

# Esta función se "dispara" CADA VEZ que una 'Review' se borra (post_delete)
@receiver(post_delete, sender=Review)
def review_deleted_handler(sender, instance, **kwargs):
    # 'instance' es la Reseña que se acaba de borrar
    update_profile_rating(instance.reviewed_profile.id)