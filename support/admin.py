from django.contrib import admin
from .models import SupportTicket, TicketMessage

# Register your models here.

# Para mostrar los mensajes "dentro" del ticket en el admin
class TicketMessageInline(admin.StackedInline):
    model = TicketMessage
    extra = 1 # Mostrar 1 campo para escribir una nueva respuesta
    readonly_fields = ('sender', 'sent_at') # No dejar editar quién lo mandó

class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'user_profile', 'status', 'priority', 'assigned_to', 'updated_at')
    list_filter = ('status', 'priority', 'assigned_to')
    search_fields = ('subject', 'user_profile__full_name')
    list_editable = ('status', 'priority', 'assigned_to')
    readonly_fields = ('user_profile',) # No se puede cambiar quién creó el ticket
    
    # ¡Aquí conectamos los mensajes!
    inlines = [TicketMessageInline]

admin.site.register(SupportTicket, SupportTicketAdmin)
# No registramos TicketMessage por separado, ya que se maneja "dentro" del Ticket