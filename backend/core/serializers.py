from rest_framework import serializers
from datetime import date
import re, unicodedata

from .models import AboutPage, Appointment, Service, Work

PHONE_RE = re.compile(r'^\+7\d{10}$')


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
        model  = Appointment
        fields = '__all__'

    def validate_name(self, value: str) -> str:
        value = value.strip()
        if not value:
            raise serializers.ValidationError('Имя не может быть пустым.')
        value = unicodedata.normalize('NFKC', re.sub(r'\s+', ' ', value))
        return value

    def validate_phone(self, value: str) -> str:
        if not PHONE_RE.fullmatch(value):
            raise serializers.ValidationError(
                'Телефон должен быть в формате +7 (123) 45 67'
            )
        return value

    def validate_preferred_date(self, value):
        if value and value < date.today():
            raise serializers.ValidationError('Нельзя выбрать дату в прошлом.')
        return value
