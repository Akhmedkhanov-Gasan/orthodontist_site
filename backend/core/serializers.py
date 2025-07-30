from rest_framework import serializers
from .models import AboutPage, Appointment, Service, Work
from datetime import date


class AboutPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutPage
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = '__all__'

    def get_image(self, obj):
        return obj.image.url if obj.image else None


class WorkSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model  = Work
        fields = "__all__"

    def get_image(self, obj):
        return obj.image.url if obj.image else None


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

    def validate_preferred_date(self, value):
        if value and value < date.today():
            raise serializers.ValidationError("Нельзя выбрать дату в прошлом.")
        return value
