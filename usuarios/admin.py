from django.contrib import admin
from .models import Role, UserProfile, DriverData, ProviderData

# Register your models here.

# Queremos ver los perfiles de forma más avanzada
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'phone', 'is_active_for_service')
    search_fields = ('full_name', 'phone', 'user__username')
    # Filtro para ver los roles
    filter_horizontal = ('roles',)

class DriverDataAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'vehicle_plate', 'dni', 'is_verified')
    search_fields = ('user_profile__full_name', 'vehicle_plate', 'dni')
    list_editable = ('is_verified',)

# Registramos los modelos en el panel de admin
admin.site.register(Role)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(DriverData, DriverDataAdmin)
admin.site.register(ProviderData)