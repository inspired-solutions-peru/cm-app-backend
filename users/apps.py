from django.apps import AppConfig


class usersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    # ¡Añadimos esta función!
    # Esto le dice a Django que cargue nuestros "signals"
    # cuando arranque la aplicación.
    def ready(self):
        import users.signals # Importa las señales