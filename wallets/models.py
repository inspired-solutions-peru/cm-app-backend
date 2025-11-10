from django.db import models
from django.conf import settings
from users.models import UserProfile # Importamos el Perfil
from django.db import transaction

# Create your models here.

# ---------------------------------------------------------------------------
# MODELO 1: BILLETERA (WALLET)
# ---------------------------------------------------------------------------
class Wallet(models.Model):
    # Cada UserProfile (sea cliente o conductor) tiene UNA billetera
    user_profile = models.OneToOneField(
        UserProfile, 
        on_delete=models.CASCADE, 
        related_name="wallet"
    )
    
    # El balance actual. Usamos DecimalField para dinero
    balance = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00,
        verbose_name="Saldo Actual"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Billetera de {self.user_profile.full_name} (Saldo: S/ {self.balance})"

    class Meta:
        verbose_name = "Billetera"
        verbose_name_plural = "Billeteras"

# ---------------------------------------------------------------------------
# MODELO 2: TRANSACCIÓN (TRANSACTION)
# ---------------------------------------------------------------------------
class Transaction(models.Model):
    
    class TransactionType(models.TextChoices):
        DEPOSIT = 'DEPOSIT', 'Depósito'     # Dinero entrando (ej. pago de viaje)
        WITHDRAWAL = 'WITHDRAWAL', 'Retiro' # Dinero saliendo (ej. conductor retira)
        BONUS = 'BONUS', 'Bono/Promoción'   # Dinero "gratis"
        REFUND = 'REFUND', 'Reembolso'     # Devolución
        FEE = 'FEE', 'Comisión'             # Comisión de la App

    class TransactionStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pendiente'
        COMPLETED = 'COMPLETED', 'Completado'
        FAILED = 'FAILED', 'Fallido'

    # Cada transacción pertenece a UNA billetera
    wallet = models.ForeignKey(
        Wallet, 
        on_delete=models.CASCADE, 
        related_name="transactions"
    )
    
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name="Monto"
    )
    
    transaction_type = models.CharField(
        max_length=20,
        choices=TransactionType.choices,
        verbose_name="Tipo de Transacción"
    )
    
    status = models.CharField(
        max_length=20,
        choices=TransactionStatus.choices,
        default=TransactionStatus.COMPLETED,
        verbose_name="Estado"
    )
    
    description = models.CharField(max_length=255, verbose_name="Descripción")
    
    # (Opcional) Podemos enlazar una transacción a un viaje específico
    # viaje = models.ForeignKey('travel.Viaje', on_delete=models.SET_NULL, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Muestra un signo +/- basado en el tipo
        sign = '+' if self.transaction_type in [self.TransactionType.DEPOSIT, self.TransactionType.BONUS, self.TransactionType.REFUND] else '-'
        return f"{self.wallet.user_profile.full_name}: {sign}S/ {self.amount} ({self.get_transaction_type_display()})"

    class Meta:
        verbose_name = "Transacción"
        verbose_name_plural = "Transacciones"
        ordering = ['-created_at'] # Las más nuevas primero

    # Lógica para actualizar la billetera automáticamente
    def save(self, *args, **kwargs):
        # Verificamos si es una transacción nueva y completada
        if self.pk is None and self.status == self.TransactionStatus.COMPLETED:
            with transaction.atomic(): # Asegura que la operación sea segura
                if self.transaction_type in [self.TransactionType.DEPOSIT, self.TransactionType.BONUS, self.TransactionType.REFUND]:
                    self.wallet.balance += self.amount
                elif self.transaction_type in [self.TransactionType.WITHDRAWAL, self.TransactionType.FEE]:
                    # En un caso real, validaríamos que haya fondos suficientes
                    if self.wallet.balance >= self.amount:
                        self.wallet.balance -= self.amount
                    else:
                        raise ValueError("Fondos insuficientes")
                
                self.wallet.save() # Guardamos el nuevo saldo en la billetera
        
        super().save(*args, **kwargs) # Guardamos la transacción