from django.urls import path
from . import views

urlpatterns = [
    path('', views.appointment_view, name='appointment'),
]