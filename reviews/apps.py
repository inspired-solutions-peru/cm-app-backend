from django.apps import AppConfig


class ReviewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reviews'
    
 # Esto le dice a Django que cargue nuestros "signals" cuando arranque
    def ready(self):
        import reviews.signals