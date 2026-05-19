from rest_framework import serializers
from datetime import date
import re, unicodedata

from .models import AboutPage, Appointment, Service, Work, HomePage,TeamMember

PHONE_RE = re.compile(r'^(?:\+7|8)\d{10}$')


class AboutPageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    team_members = serializers.SerializerMethodField()

    class Meta:
        model = AboutPage
        fields = "__all__"

    def get_image(self, obj):
        return obj.image.url if obj.image else None

    def get_team_members(self, obj):
        members = TeamMember.objects.filter(is_active=True)
        return TeamMemberSerializer(members, many=True).data


class HomePageSerializer(serializers.ModelSerializer):
    hero_image = serializers.SerializerMethodField()

    class Meta:
        model = HomePage
        fields = "__all__"

    def get_hero_image(self, obj):
        return obj.hero_image.url if obj.hero_image else None


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
                'Неверный формат номера телефона'
            )
        return value

    def validate_preferred_date(self, value):
        if value and value < date.today():
            raise serializers.ValidationError('Нельзя выбрать дату в прошлом.')
        return value


class TeamMemberSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()
    experience_years = serializers.IntegerField(read_only=True)

    class Meta:
        model = TeamMember
        fields = "__all__"

    def get_photo(self, obj):
        return obj.photo.url if obj.photo else None