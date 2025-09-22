from django.contrib import admin

from .models import Wallet, WalletOperation


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = (
        "uuid",
        "balance",
        "currency",
        "created_at",
        "updated_at",
        )
    search_fields = (
        "uuid",
        )
    ordering = (
        "-created_at",
        )


@admin.register(WalletOperation)
class WalletOperationAdmin(admin.ModelAdmin):
    list_display = (
        "uuid",
        "wallet",
        "operation_type",
        "amount",
        "created_at",
        )
    search_fields = (
        "uuid",
        "wallet",
        "operation_type",
        )
    list_filter = (
        "operation_type",
        "created_at",
        )
    ordering = (
        "-created_at",
        )
