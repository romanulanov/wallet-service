import uuid
from decimal import Decimal

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from .models import Wallet, WalletOperation


@pytest.mark.django_db
def test_create_wallet():
    client = APIClient()
    wallet = Wallet.objects.create(balance=500, currency="RUB")
    url = reverse("wallet_balance", args=[wallet.uuid])
    response = client.get(url, format="json")

    assert response.status_code == 200
    assert response.data["balance"] == "500.00"
    assert response.data["currency"] == "RUB"


@pytest.mark.django_db
def test_create_blank_wallet():
    client = APIClient()
    wallet = Wallet.objects.create(currency="RUB")
    url = reverse("wallet_balance", args=[wallet.uuid])
    response = client.get(url, format="json")

    assert response.status_code == 200
    assert response.data["balance"] == "0.00"


@pytest.mark.django_db
def test_get_nonexistent_wallet():
    client = APIClient()
    fake_id = uuid.uuid4()
    url = reverse("wallet_balance", args=[fake_id])
    response = client.get(url, format="json")

    assert response.status_code == 404


@pytest.mark.django_db
def test_wallet_deposit():
    client = APIClient()
    wallet = Wallet.objects.create(balance=500, currency="RUB")

    url = reverse("wallet_operation", args=[wallet.uuid])
    payload = {"operation_type": "DEPOSIT", "amount": 1000}
    response = client.post(url, payload, format="json")
    wallet.refresh_from_db()

    assert response.status_code == 200
    assert WalletOperation.objects.count() == 1
    assert wallet.balance == Decimal("1500.00")


@pytest.mark.django_db
def test_wallet_withdraw():
    client = APIClient()
    wallet = Wallet.objects.create(balance=500, currency="RUB")

    url = reverse("wallet_operation", args=[wallet.uuid])
    payload = {"operation_type": "WITHDRAW", "amount": 400}
    response = client.post(url, payload, format="json")
    wallet.refresh_from_db()

    assert response.status_code == 200
    assert WalletOperation.objects.count() == 1
    assert wallet.balance == Decimal("100.00")


@pytest.mark.django_db
def test_withdraw_more_than_balance():
    client = APIClient()
    wallet = Wallet.objects.create(balance=500, currency="RUB")

    url = reverse("wallet_operation", args=[wallet.uuid])
    payload = {"operation_type": "WITHDRAW", "amount": 600}
    response = client.post(url, payload, format="json")
    wallet.refresh_from_db()

    assert response.status_code == 400


@pytest.mark.django_db
def test_unknown_operation_type():
    client = APIClient()
    wallet = Wallet.objects.create(balance=500, currency="RUB")

    url = reverse("wallet_operation", args=[wallet.uud])
    payload = {"operation_type": "TEST", "amount": 600}
    response = client.post(url, payload, format="json")
    wallet.refresh_from_db()

    assert response.status_code == 400
    assert wallet.balance == 500
    assert WalletOperation.objects.count() == 0


@pytest.mark.django_db
def test_several_operations():
    client = APIClient()
    wallet = Wallet.objects.create(balance=500, currency="RUB")

    url = reverse("wallet_operation", args=[wallet.uuid])
    payload = {"operation_type": "DEPOSIT", "amount": 1000}
    response = client.post(url, payload, format="json")
    payload = {"operation_type": "WITHDRAW", "amount": 100}
    response = client.post(url, payload, format="json")
    wallet.refresh_from_db()

    assert response.status_code == 200
    assert WalletOperation.objects.count() == 2
    assert wallet.balance == Decimal("1400.00")


@pytest.mark.django_db
def test_deposit_negative_amount_returns_400():
    client = APIClient()
    wallet = Wallet.objects.create(balance=500, currency="RUB")

    url = reverse("wallet_operation", args=[wallet.uuid])
    payload = {"operation_type": "DEPOSIT", "amount": -100}
    response = client.post(url, payload, format="json")
    wallet.refresh_from_db()

    assert response.status_code == 400
    assert wallet.balance == 500
    assert WalletOperation.objects.count() == 0


@pytest.mark.django_db
def test_withdraw_negative_amount_returns_400():
    client = APIClient()
    wallet = Wallet.objects.create(balance=500, currency="RUB")

    url = reverse("wallet_operation", args=[wallet.uuid])
    payload = {"operation_type": "WITHDRAW", "amount": -200}
    response = client.post(url, payload, format="json")
    wallet.refresh_from_db()

    assert response.status_code == 400
    assert wallet.balance == 500
    assert WalletOperation.objects.count() == 0
