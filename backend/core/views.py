from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.db import connection
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie


from .models import Service, Appointment, AboutPage, Work
from .serializers import (
    ServiceSerializer,
    AppointmentSerializer,
    AboutPageSerializer,
    WorkSerializer
)
from .utils import verify_recaptcha

class ServiceListView(APIView):
    def get(self, request):
        services = Service.objects.all()
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AppointmentCreateView(APIView):
    """
    Публичная форма записи.
    Требует:
      - корректный CSRF-token (браузер шлёт cookie + заголовок)
      - валидный reCAPTCHA v3 token в поле  `recaptcha_token`
    Ограничено 5 запросами в минуту анонимно (AnonRateThrottle).
    """

    def post(self, request):
        if not verify_recaptcha(
                request.data.get("recaptcha_token"),
                request.META.get("REMOTE_ADDR")
        ):
            return Response(
                {"detail": "reCAPTCHA failed"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AboutPageDetail(APIView):
    def get(self, request):
        about_page = AboutPage.objects.first()
        if not about_page:
            return Response({"detail": "Not found."},
                            status=status.HTTP_404_NOT_FOUND)
        serializer = AboutPageSerializer(about_page)
        return Response(serializer.data, status=status.HTTP_200_OK)


class WorkListView(APIView):
    def get(self, request):
        works = Work.objects.all()
        serializer = WorkSerializer(works, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@ensure_csrf_cookie
def csrf(request):
    return JsonResponse({"ok": True})

def health(request):
    try:
        connection.ensure_connection()
    except Exception:
        return HttpResponse("db_error", status=500)

    return HttpResponse("ok", status=200)
