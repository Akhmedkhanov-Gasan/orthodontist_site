from django.urls import path
from .views import (
    ServiceListView,
    AppointmentCreateView,
    AboutPageDetail,
    WorkListView,
    csrf,
    health,
    ping,
)

urlpatterns = [
    path('services/', ServiceListView.as_view(), name='services-list'),
    path('appointments/', AppointmentCreateView.as_view(), name='appointment-create'),
    path('about/', AboutPageDetail.as_view(), name='about-page'),
    path('works/', WorkListView.as_view(), name='works-list'),
    path('csrf/', csrf, name='csrf'),
    path("ping/", ping,   name="ping"),
    path("health/", health, name="health"),
]
