from django.shortcuts import render


def index(request):
    return render(request, 'index.html')  # Соответствует пути '' в urls.py


def about(request):
    return render(request, 'about.html')  # Соответствует пути 'about/' в urls.py


def appointment(request):
    return render(request, 'appointment.html')  # Соответствует пути 'appointment/' в urls.py


def contact(request):
    return render(request, 'contact.html')  # Соответствует пути 'contact/' в urls.py


def price(request):
    return render(request, 'price.html')  # Соответствует пути 'price/' в urls.py


def service(request):
    return render(request, 'service.html')  # Соответствует пути 'service/' в urls.py


def team(request):
    return render(request, 'team.html')  # Соответствует пути 'team/' в urls.py


def testimonial(request):
    return render(request, 'testimonial.html')  # Соответствует пути 'testimonial/' в urls.py
