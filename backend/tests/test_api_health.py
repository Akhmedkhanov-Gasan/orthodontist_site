import pytest
from django.urls import reverse
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


def test_ping_returns_pong(api_client):
    response = api_client.get(reverse("ping"))

    assert response.status_code == 200
    assert response.content == b"pong"


@pytest.mark.django_db
def test_health_returns_ok_when_database_is_available(api_client):
    response = api_client.get(reverse("health"))

    assert response.status_code == 200
    assert response.content == b"ok"


def test_csrf_returns_ok(api_client):
    response = api_client.get(reverse("csrf"))

    assert response.status_code == 200
    assert response.json() == {"ok": True}