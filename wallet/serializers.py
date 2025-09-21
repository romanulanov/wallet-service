from rest_framework import serializers
from .models import Wallet, WalletOperation


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ("id", "balance", "currency")


class WalletOperationSerializer(serializers.Serializer):
    operation_type = serializers.ChoiceField(choices=WalletOperation.OPERATION_CHOICES)
    amount = serializers.DecimalField(max_digits=20, decimal_places=2)
