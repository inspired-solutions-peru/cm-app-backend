# users/signals.py (CÓDIGO CORREGIDO CON LÓGICA COMENTADA)

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

# from wallets.models import Wallet # <-- ¡COMENTADO! Esta línea causaba el error circular.

import logging
logger = logging.getLogger(__name__)

# -----------------------------------------------------------------
# SEÑAL 1: Crea el UserProfile cuando se crea un User (¡VITAL!)
# -----------------------------------------------------------------
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Crea automáticamente un UserProfile cuando un nuevo User es creado.
    """
    if created:
        try:
            UserProfile.objects.create(user=instance)
            logger.info(f"UserProfile creado para el usuario: {instance.username}")
        except Exception as e:
            logger.error(f"Error al crear UserProfile para {instance.username}: {e}")

# -----------------------------------------------------------------
# SEÑAL 2: Crea la Wallet cuando se crea un UserProfile (¡COMENTADA!)
# -----------------------------------------------------------------
@receiver(post_save, sender=UserProfile)
def create_user_wallet(sender, instance, created, **kwargs):
    """
    Crea automáticamente una Wallet para un UserProfile nuevo.
    (Función deshabilitada temporalmente. Se activará en el futuro
    cuando el frontend tenga la sección de Billetera).
    """
    if created:
        
        # --- LÓGICA DE BILLETERA (COMENTADA HASTA NUEVO AVISO) ---
        
        # try:
        #     # Importamos aquí dentro para evitar errores circulares
        #     from wallets.models import Wallet
        #     Wallet.objects.create(user_profile=instance)
        #     logger.info(f"Wallet creada para el perfil: {instance.id}")
        # except Exception as e:
        #     logger.error(f"Error al crear Wallet para el perfil {instance.id}: {e}")
        
        # --- FIN DE LÓGICA DE BILLETERA ---
        
        logger.warning(f"Señal create_user_wallet disparada para {instance.id}, pero la lógica está comentada.")
        pass # No hacer nada por ahora.