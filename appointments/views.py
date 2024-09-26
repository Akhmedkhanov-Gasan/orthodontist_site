import os
from datetime import datetime
from django.conf import settings
from django.shortcuts import render
import requests
from dotenv import load_dotenv

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
            raise Exception(f"Error sending message: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Failed to send message to Telegram: {e}")


def appointment_view(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        contact_info = request.POST.get('contact_info')
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')

        file_path = os.path.join(settings.BASE_DIR, 'appointments.txt')
        with open(file_path, 'a', encoding='utf-8') as file:
            file.write(f"{datetime.now()} - Name: {full_name}, Contact Info: {contact_info}, "
                       f"Appointment Date: {appointment_date}, Appointment Time: {appointment_time}\n")

        message = (f"New appointment:\n"
                   f"Name: {full_name}\n"
                   f"Contact Info: {contact_info}\n"
                   f"Appointment Date: {appointment_date}\n"
                   f"Appointment Time: {appointment_time}")
        send_telegram_message(message)

        return render(request, 'appointment.html')

    return render(request, 'appointment.html')
