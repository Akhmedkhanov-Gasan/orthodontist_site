import os
from datetime import datetime
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render


def appointment_view(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        contact_info = request.POST.get('contact_info')
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')
        file_path = os.path.join(settings.BASE_DIR, 'appointments.txt')
        with open(file_path, 'a', encoding='utf-8') as file:
            file.write(f"{datetime.now()} - Name: {full_name}, Contact Info: {contact_info}, Appointment Date: {appointment_date}, Appointment Time: {appointment_time}\n")

        # return HttpResponse("Appointment has been successfully recorded.")
        return render(request, 'appointment.html')

    return render(request, 'appointment.html')
