from core.models import Appointment, Patient

from datetime import date, datetime


def create_or_update_patient_from_telegram(
    *,
    telegram_id,
    telegram_username,
    full_name,
    phone,
):
    patient, created = Patient.objects.update_or_create(
        telegram_id=telegram_id,
        defaults={
            "telegram_username": telegram_username or "",
            "full_name": full_name,
            "phone": phone,
            "is_active": True,
        },
    )

    return patient, created


def format_new_patient_admin_message(patient, created):
    status = "Новый пациент" if created else "Пациент обновил данные"

    username = patient.telegram_username
    username_line = f"@{username}" if username else "не указан"

    return (
        f"{status}\n\n"
        f"Имя: {patient.full_name}\n"
        f"Телефон: {patient.phone}\n"
        f"Telegram: {username_line}\n"
        f"Telegram ID: {patient.telegram_id}"
    )


def get_patient_by_telegram_id(telegram_id):
    return Patient.objects.filter(telegram_id=telegram_id, is_active=True).first()


def create_appointment_for_patient(*, patient, preferred_date):
    return Appointment.objects.create(
        patient=patient,
        name=patient.full_name,
        phone=patient.phone or "",
        preferred_date=preferred_date,
        status="new",
    )


def parse_appointment_date(value):
    try:
        parsed_date = datetime.strptime(value.strip(), "%d.%m.%Y").date()
    except ValueError:
        return None, "invalid_format"

    if parsed_date < date.today():
        return None, "past_date"

    return parsed_date, None
