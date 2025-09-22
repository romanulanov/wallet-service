from decimal import Decimal

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Wallet
from .serializers import WalletOperationSerializer, WalletSerializer


class WalletDetailsView(APIView):
    def get(self, request, wallet_id):
        wallet = get_object_or_404(Wallet, pk=wallet_id)
        serializer = WalletSerializer(wallet)
        return Response(serializer.data)


class WalletOperationView(APIView):
    def post(self, request, wallet_id):
        wallet = get_object_or_404(Wallet, pk=wallet_id)
        serializer = WalletOperationSerializer(data=request.data)

        if serializer.is_valid():
            operation_type = serializer.validated_data["operation_type"]
            amount = serializer.validated_data["amount"]

            try:
                wallet.change_balance(operation_type, Decimal(amount))
            except Exception as e:
                return Response(
                    {
                        "error": str(e)
                    },
                    status=status.HTTP_400_BAD_REQUEST
                    )

            return Response(WalletSerializer(wallet).data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
