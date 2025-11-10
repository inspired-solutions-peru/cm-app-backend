from django.contrib import admin
# ¡Añade los nuevos modelos a la importación!
from .models import (
    Role, 
    UserProfile, 
    DriverData, 
    ProviderData, 
    UserSavedLocation,
    PaymentMethodType,  
    UserPaymentMethod   
)

# Register your models here.

# --- ADMINS EXISTENTES ---
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user', 
        'full_name', 
        'phone', 
        'is_active_for_service', 
        'average_rating', 
        'total_ratings'    
    )
    search_fields = ('full_name', 'phone', 'user__username')
    filter_horizontal = ('roles',)

class DriverDataAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'vehicle_plate', 'dni', 'is_verified')
    search_fields = ('user_profile__full_name', 'vehicle_plate', 'dni')
    list_editable = ('is_verified',)

# --- ADMINS NUEVOS ---
class UserPaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'payment_type', 'card_brand', 'last_four_digits', 'identifier', 'is_default')
    list_filter = ('payment_type', 'card_brand', 'is_default')
    search_fields = ('user_profile__full_name', 'identifier', 'last_four_digits')

# Registramos los modelos en el panel de admin
admin.site.register(Role)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(DriverData, DriverDataAdmin)
admin.site.register(ProviderData)
admin.site.register(UserSavedLocation) # <-- Este lo añadimos en el Paso 1

# --- REGISTROS NUEVOS ---
admin.site.register(PaymentMethodType)
admin.site.register(UserPaymentMethod, UserPaymentMethodAdmin)