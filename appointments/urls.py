from django.urls import path
from . import views

urlpatterns = [
    path('', views.appointment_view, name='appointment'),
    path('success/', views.appointment_success_view, name='appointment_success'),
]