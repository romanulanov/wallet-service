import uuid
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models


class Wallet(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )
    balance = models.DecimalField(
        verbose_name="Баланс",
        max_digits=20,
        decimal_places=2,
        default=0,
    )
    currency = models.CharField(
        verbose_name="Валюта",
        max_length=3,
        default="RUB",
    )
    created_at = models.DateTimeField(
        verbose_name="Создан",
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name="Обновлен",
        auto_now=True
    )

    class Meta:
        verbose_name = "Счет"
        verbose_name_plural = "Счета"

    def change_balance(self, operation_type: str, amount: Decimal):
        if amount <= 0:
            raise ValidationError("Сумма должна быть больше 0")

        if operation_type == "DEPOSIT":
            self.balance += amount
        elif operation_type == "WITHDRAW":
            if self.balance < amount:
                raise ValidationError("Недостаточно средсв")
            self.balance -= amount
        else:
            raise ValidationError("Неверный тип операции")

        self.save()
        WalletOperation.objects.create(
            wallet=self,
            operation_type=operation_type,
            amount=amount,
        )

    def __str__(self):
        return f"Счет №{str(self.uuid)}"


class WalletOperation(models.Model):
    OPERATION_CHOICES = [
        ("DEPOSIT", "Пополнение"),
        ("WITHDRAW", "Списание"),
    ]

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    wallet = models.ForeignKey(
        Wallet,
        verbose_name="Счет",
        on_delete=models.CASCADE,
        related_name="operations",
    )

    operation_type = models.CharField(
        verbose_name="Тип операции",
        max_length=10,
        choices=OPERATION_CHOICES,
    )

    amount = models.DecimalField(
        verbose_name="Сумма операции",
        max_digits=20,
        decimal_places=2,
    )

    created_at = models.DateTimeField(
        verbose_name="Дата операции",
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "Операция",
        verbose_name_plural = "Операции"

    def __str__(self):
        return f"Операция {self.operation_type} №{str(self.uuid)[-6:]} \
            cо счета {self.wallet.uuid} на сумму {self.amount}"
