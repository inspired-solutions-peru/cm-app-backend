from django.db import models
from django.conf import settings
from users.models import UserProfile # Importamos el Perfil

# Create your models here.

# ---------------------------------------------------------------------------
# MODELO 1: TICKET DE SOPORTE
# ---------------------------------------------------------------------------
class SupportTicket(models.Model):
    
    class TicketStatus(models.TextChoices):
        OPEN = 'OPEN', 'Abierto'
        IN_PROGRESS = 'IN_PROGRESS', 'En Progreso'
        CLOSED = 'CLOSED', 'Cerrado'

    class TicketPriority(models.TextChoices):
        LOW = 'LOW', 'Baja'
        MEDIUM = 'MEDIUM', 'Media'
        HIGH = 'HIGH', 'Alta'

    # Qué usuario creó el ticket
    user_profile = models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL, # Si se borra el user, el ticket queda (para historial)
        null=True,
        related_name="support_tickets"
    )
    
    subject = models.CharField(max_length=255, verbose_name="Asunto")
    
    status = models.CharField(
        max_length=20,
        choices=TicketStatus.choices,
        default=TicketStatus.OPEN,
        verbose_name="Estado"
    )
    
    priority = models.CharField(
        max_length=20,
        choices=TicketPriority.choices,
        default=TicketPriority.MEDIUM,
        verbose_name="Prioridad"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # (Opcional) Quién del staff (admin) está asignado a este ticket
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="assigned_tickets",
        limit_choices_to={'is_staff': True} # Solo se puede asignar a admins
    )

    def __str__(self):
        return f"Ticket #{self.id} ({self.subject}) - {self.get_status_display()}"

    class Meta:
        verbose_name = "Ticket de Soporte"
        verbose_name_plural = "Tickets de Soporte"
        ordering = ['-updated_at']

# ---------------------------------------------------------------------------
# MODELO 2: MENSAJE DEL TICKET (LA CONVERSACIÓN)
# ---------------------------------------------------------------------------
class TicketMessage(models.Model):
    ticket = models.ForeignKey(
        SupportTicket,
        on_delete=models.CASCADE,
        related_name="messages"
    )
    
    # Quién envió el mensaje (el usuario del perfil o un admin)
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Remitente"
    )
    
    message = models.TextField(verbose_name="Mensaje")
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mensaje de {self.sender.username} en Ticket #{self.ticket.id}"

    class Meta:
        verbose_name = "Mensaje de Ticket"
        verbose_name_plural = "Mensajes de Tickets"
        ordering = ['sent_at'] # El más antiguo primero, para leer como chat    