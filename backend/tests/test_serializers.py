from datetime import timedelta

import pytest
from django.utils import timezone

from core.serializers import AppointmentSerializer


def valid_appointment_data(**overrides):
    data = {
        "name": "Иван Иванов",
        "phone": "+79991234567",
        "message": "Хочу записаться",
        "preferred_date": timezone.localdate() + timedelta(days=1),
    }
    data.update(overrides)
    return data


@pytest.mark.django_db
def test_appointment_serializer_accepts_valid_data():
    serializer = AppointmentSerializer(data=valid_appointment_data())

    assert serializer.is_valid(), serializer.errors


@pytest.mark.django_db
def test_appointment_serializer_normalizes_name_spaces():
    serializer = AppointmentSerializer(
        data=valid_appointment_data(name="  Иван   Иванов  ")
    )

    assert serializer.is_valid(), serializer.errors
    assert serializer.validated_data["name"] == "Иван Иванов"


@pytest.mark.django_db
@pytest.mark.parametrize("name", ["", "   "])
def test_appointment_serializer_rejects_empty_name(name):
    serializer = AppointmentSerializer(data=valid_appointment_data(name=name))

    assert not serializer.is_valid()
    assert "name" in serializer.errors


@pytest.mark.django_db
@pytest.mark.parametrize("phone", ["+79991234567", "89991234567"])
def test_appointment_serializer_accepts_valid_russian_phone(phone):
    serializer = AppointmentSerializer(data=valid_appointment_data(phone=phone))

    assert serializer.is_valid(), serializer.errors


@pytest.mark.django_db
@pytest.mark.parametrize(
    "phone",
    [
        "+7999123456",
        "+799912345678",
        "79991234567",
        "+1 999 123 45 67",
        "not-a-phone",
    ],
)
def test_appointment_serializer_rejects_invalid_phone(phone):
    serializer = AppointmentSerializer(data=valid_appointment_data(phone=phone))

    assert not serializer.is_valid()
    assert "phone" in serializer.errors


@pytest.mark.django_db
def test_appointment_serializer_rejects_past_preferred_date():
    yesterday = timezone.localdate() - timedelta(days=1)

    serializer = AppointmentSerializer(
        data=valid_appointment_data(preferred_date=yesterday)
    )

    assert not serializer.is_valid()
    assert "preferred_date" in serializer.errors


@pytest.mark.django_db
def test_appointment_serializer_accepts_today_preferred_date():
    serializer = AppointmentSerializer(
        data=valid_appointment_data(preferred_date=timezone.localdate())
    )

    assert serializer.is_valid(), serializer.errors