from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('index.html', views.index, name='home'),
    path('about.html', views.about, name='about'),
    path('contact.html', views.contact, name='contact'),
    path('price.html', views.price, name='price'),
    path('testimonial.html', views.testimonial, name='testimonial'),
    path('appointments/', include('appointments.urls')),
]
