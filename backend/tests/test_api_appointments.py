from datetime import timedelta

import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient

from core.models import Appointment


@pytest.fixture
def api_client():
    return APIClient()


def appointment_payload(**overrides):
    data = {
        "name": "Иван Иванов",
        "phone": "+79991234567",
        "message": "Хочу записаться на консультацию",
        "preferred_date": (timezone.localdate() + timedelta(days=1)).isoformat(),
        "recaptcha_token": "valid-token",
    }
    data.update(overrides)
    return data


@pytest.mark.django_db
def test_create_appointment_success(api_client, monkeypatch):
    monkeypatch.setenv("DISABLE_RECAPTCHA", "0")
    monkeypatch.setattr("core.views.verify_recaptcha", lambda token, remote_ip=None: True)

    response = api_client.post(
        reverse("appointment-create"),
        appointment_payload(),
        format="json",
    )

    assert response.status_code == 201
    assert Appointment.objects.count() == 1

    appointment = Appointment.objects.get()
    assert appointment.name == "Иван Иванов"
    assert appointment.phone == "+79991234567"
    assert appointment.status == "new"


@pytest.mark.django_db
def test_create_appointment_returns_400_when_recaptcha_fails(api_client, monkeypatch):
    monkeypatch.setenv("DISABLE_RECAPTCHA", "0")
    monkeypatch.setattr("core.views.verify_recaptcha", lambda token, remote_ip=None: False)

    response = api_client.post(
        reverse("appointment-create"),
        appointment_payload(),
        format="json",
    )

    assert response.status_code == 400
    assert response.data == {"detail": "reCAPTCHA failed"}
    assert Appointment.objects.count() == 0


@pytest.mark.django_db
def test_create_appointment_returns_400_when_payload_is_invalid(api_client, monkeypatch):
    monkeypatch.setenv("DISABLE_RECAPTCHA", "0")
    monkeypatch.setattr("core.views.verify_recaptcha", lambda token, remote_ip=None: True)

    response = api_client.post(
        reverse("appointment-create"),
        appointment_payload(phone="invalid-phone"),
        format="json",
    )

    assert response.status_code == 400
    assert "phone" in response.data
    assert Appointment.objects.count() == 0