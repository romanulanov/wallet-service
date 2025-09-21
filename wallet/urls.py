from django.urls import path
from .views import WalletDetailsView, WalletOperationView

urlpatterns = [
    path(
        "wallets/<uuid:wallet_id>/",
        WalletDetailsView.as_view(),
        name="wallet_balance"),
    path(
        "wallets/<uuid:wallet_id>/operation/",
        WalletOperationView.as_view(),
        name="wallet_operation"),
]