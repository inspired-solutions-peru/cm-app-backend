from django.contrib import admin
from .models import PromoCode, UserPromoCodeUsage

# Register your models here.

class PromoCodeAdmin(admin.ModelAdmin):
    list_display = (
        'code', 
        'discount_type', 
        'discount_value', 
        'is_active', 
        'valid_from', 
        'valid_to', 
        'max_uses', 
        'uses_per_user'
    )
    list_filter = ('is_active', 'discount_type')
    search_fields = ('code', 'description')

class UserPromoCodeUsageAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'promo_code', 'used_at', 'viaje')
    search_fields = ('user_profile__full_name', 'promo_code__code')
    autocomplete_fields = ('user_profile', 'promo_code', 'viaje') # Facilita la búsqueda

admin.site.register(PromoCode, PromoCodeAdmin)
admin.site.register(UserPromoCodeUsage, UserPromoCodeUsageAdmin)