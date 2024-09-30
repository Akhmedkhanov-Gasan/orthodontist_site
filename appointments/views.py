from django.shortcuts import render, redirect
from main.models import Doctor
import os
from datetime import datetime
from django.conf import settings
from dotenv import load_dotenv
import requests

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')


def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            raise Exception(
                f"Error sending message: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Failed to send message to Telegram: {e}")


def appointment_view(request):
    doctors = Doctor.objects.all()

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        contact_info = request.POST.get('contact_info')
        appointment_datetime = request.POST.get('appointment_datetime')
        doctor_id = request.POST.get('doctor')

        doctor = Doctor.objects.get(id=doctor_id)

        file_path = os.path.join(settings.BASE_DIR, 'appointments.txt')
        with open(file_path, 'a', encoding='utf-8') as file:
            file.write(
                f"{datetime.now()} - ФИГ: {full_name}, Контактная информация: {contact_info}, "
                f"Дата на которую пациент хочет записаться: {appointment_datetime}, Доктор: {doctor.full_name}\n")

        message = (f"Новая запись:\n"
                   f"ФИО: {full_name}\n"
                   f"Контактная информация: {contact_info}\n"
                   f"Дата на которую пациент хочет записаться: {appointment_datetime}\n"
                   f"Доктор: {doctor.full_name}")
        send_telegram_message(message)

        return redirect('appointment_success')

    return render(request, 'appointment.html', {'doctors': doctors})


def appointment_success_view(request):
    return render(request, 'includes/appointment_success.html')

