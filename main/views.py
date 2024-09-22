from django.shortcuts import render


def index(request):
    return render(request, 'index.html', {'active_page': 'home'})


def about(request):
    return render(request, 'about.html', {'active_page': 'about'})


def appointment(request):
    return render(request, 'appointment.html', {'active_page': 'appointment'})


def contact(request):
    return render(request, 'contact.html', {'active_page': 'contact'})


def price(request):
    return render(request, 'price.html', {'active_page': 'price'})


def service(request):
    return render(request, 'service.html', {'active_page': 'service'})


def team(request):
    return render(request, 'team.html', {'active_page': 'team'})


def testimonial(request):
    return render(request, 'testimonial.html', {'active_page': 'testimonial'})
