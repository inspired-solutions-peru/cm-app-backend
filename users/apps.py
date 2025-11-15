# users/apps.py (ASEGÚRATE QUE ESTÉ ASÍ)

from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        # Importa los signals aquí para que se registren
        # cuando Django arranque.
        try:
            import users.signals
        except ImportError:
            pass