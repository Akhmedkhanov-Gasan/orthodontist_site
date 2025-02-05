from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .models import Service, Appointment, AboutPage, Work
from .serializers import (
    ServiceSerializer,
    AppointmentSerializer,
    AboutPageSerializer,
    WorkSerializer
)


class ServiceListView(APIView):
    def get(self, request):
        services = Service.objects.all()
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class AppointmentCreateView(APIView):
    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            appointment = serializer.save()
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