from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('index.html', views.index, name='home'),
    path('about.html', views.about, name='about'),
    path('appointment.html', views.appointment, name='appointment'),
    path('contact.html', views.contact, name='contact'),
    path('price.html', views.price, name='price'),
    path('service.html', views.service, name='service'),
    path('team.html', views.team, name='team'),
    path('testimonial.html', views.testimonial, name='testimonial'),
]
