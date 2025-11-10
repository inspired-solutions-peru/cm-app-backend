from django.contrib import admin
from .models import Review

# Register your models here.

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'reviewer_profile', 'reviewed_profile', 'rating', 'viaje', 'created_at')
    list_filter = ('rating',)
    search_fields = ('reviewer_profile__full_name', 'reviewed_profile__full_name', 'comment')
    # Hacemos los campos de relación "leíbles" y no editables
    readonly_fields = ('reviewer_profile', 'reviewed_profile', 'viaje')

admin.site.register(Review, ReviewAdmin)