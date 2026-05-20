from datetime import timedelta

import pytest
from django.utils import timezone

from core.bot.services import (
    create_appointment_for_patient,
    create_or_update_patient_from_telegram,
    get_patient_by_telegram_id,
    parse_appointment_date,
)
from core.models import Appointment, Patient


@pytest.mark.parametrize(
    ("value", "expected_error"),
    [
        ("20-05-2026", "invalid_format"),
        ("not-a-date", "invalid_format"),
        ("", "invalid_format"),
    ],
)
def test_parse_appointment_date_returns_invalid_format_for_wrong_format(
    value,
    expected_error,
):
    parsed_date, error = parse_appointment_date(value)

    assert parsed_date is None
    assert error == expected_error


def test_parse_appointment_date_returns_past_date_for_past_date():
    yesterday = timezone.localdate() - timedelta(days=1)

    parsed_date, error = parse_appointment_date(yesterday.strftime("%d.%m.%Y"))

    assert parsed_date is None
    assert error == "past_date"


def test_parse_appointment_date_returns_date_for_valid_future_date():
    tomorrow = timezone.localdate() + timedelta(days=1)

    parsed_date, error = parse_appointment_date(tomorrow.strftime("%d.%m.%Y"))

    assert parsed_date == tomorrow
    assert error is None


@pytest.mark.django_db
def test_create_or_update_patient_from_telegram_creates_patient():
    patient, created = create_or_update_patient_from_telegram(
        telegram_id=123456,
        telegram_username="ivan",
        full_name="Иван Иванов",
        phone="+79991234567",
    )

    assert created is True
    assert patient.telegram_id == 123456
    assert patient.telegram_username == "ivan"
    assert patient.full_name == "Иван Иванов"
    assert patient.phone == "+79991234567"
    assert patient.is_active is True
    assert Patient.objects.count() == 1


@pytest.mark.django_db
def test_create_or_update_patient_from_telegram_updates_existing_patient():
    Patient.objects.create(
        telegram_id=123456,
        telegram_username="old_username",
        full_name="Старое имя",
        phone="+79990000000",
        is_active=False,
    )

    patient, created = create_or_update_patient_from_telegram(
        telegram_id=123456,
        telegram_username="new_username",
        full_name="Новое имя",
        phone="+79991234567",
    )

    assert created is False
    assert Patient.objects.count() == 1

    patient.refresh_from_db()
    assert patient.telegram_username == "new_username"
    assert patient.full_name == "Новое имя"
    assert patient.phone == "+79991234567"
    assert patient.is_active is True


@pytest.mark.django_db
def test_create_or_update_patient_from_telegram_stores_empty_username_when_missing():
    patient, created = create_or_update_patient_from_telegram(
        telegram_id=123456,
        telegram_username=None,
        full_name="Иван Иванов",
        phone="+79991234567",
    )

    assert created is True
    assert patient.telegram_username == ""


@pytest.mark.django_db
def test_get_patient_by_telegram_id_returns_active_patient():
    active_patient = Patient.objects.create(
        telegram_id=123456,
        full_name="Активный пациент",
        is_active=True,
    )

    result = get_patient_by_telegram_id(123456)

    assert result == active_patient


@pytest.mark.django_db
def test_get_patient_by_telegram_id_ignores_inactive_patient():
    Patient.objects.create(
        telegram_id=123456,
        full_name="Неактивный пациент",
        is_active=False,
    )

    result = get_patient_by_telegram_id(123456)

    assert result is None


@pytest.mark.django_db
def test_create_appointment_for_patient_creates_new_appointment():
    preferred_date = timezone.localdate() + timedelta(days=1)
    patient = Patient.objects.create(
        telegram_id=123456,
        full_name="Иван Иванов",
        phone="+79991234567",
    )

    appointment = create_appointment_for_patient(
        patient=patient,
        preferred_date=preferred_date,
    )

    assert Appointment.objects.count() == 1
    assert appointment.patient == patient
    assert appointment.name == "Иван Иванов"
    assert appointment.phone == "+79991234567"
    assert appointment.preferred_date == preferred_date
    assert appointment.status == "new"


@pytest.mark.django_db
def test_create_appointment_for_patient_uses_empty_phone_when_patient_phone_is_missing():
    patient = Patient.objects.create(
        telegram_id=123456,
        full_name="Иван Иванов",
        phone=None,
    )

    appointment = create_appointment_for_patient(
        patient=patient,
        preferred_date=None,
    )

    assert appointment.phone == ""
    assert appointment.preferred_date is None