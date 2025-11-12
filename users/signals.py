from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile
from wallets.models import Wallet # Importar el modelo Wallet

import logging
logger = logging.getLogger(__name__)

# Esta señal se "dispara" CADA VEZ que un 'UserProfile' se guarda POR PRIMERA VEZ
@receiver(post_save, sender=UserProfile)
def create_user_wallet(sender, instance, created, **kwargs):
    """
    Crea automáticamente una Wallet para un UserProfile nuevo.
    """
    if created:
        try:
            Wallet.objects.create(user_profile=instance)
            logger.info(f"Wallet creada para el perfil: {instance.id}")
        except Exception as e:
            logger.error(f"Error al crear Wallet para el perfil {instance.id}: {e}")