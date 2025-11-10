from django.contrib import admin
from .models import Wallet, Transaction

# Register your models here.

class WalletAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_profile', 'balance', 'updated_at')
    search_fields = ('user_profile__full_name', 'user_profile__user__username')
    readonly_fields = ('balance', 'created_at', 'updated_at') # El saldo solo se edita con transacciones

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'wallet', 'amount_display', 'transaction_type', 'status', 'description', 'created_at')
    list_filter = ('transaction_type', 'status')
    search_fields = ('wallet__user_profile__full_name', 'description')
    
    # Función para mostrar el monto con su signo +/-
    def amount_display(self, obj):
        if obj.transaction_type in [Transaction.TransactionType.DEPOSIT, Transaction.TransactionType.BONUS, Transaction.TransactionType.REFUND]:
            return f"+ S/ {obj.amount}"
        return f"- S/ {obj.amount}"
    amount_display.short_description = "Monto"

admin.site.register(Wallet, WalletAdmin)
admin.site.register(Transaction, TransactionAdmin)