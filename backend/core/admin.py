from django.contrib import admin
from .models import (
    Patient, PatientImage,
    Appointment,
    Service,
    Work,
    AboutPage,
)
from django.utils.html import format_html


class PatientImageInline(admin.TabularInline):
    model = PatientImage
    extra = 1

    readonly_fields = ('image_preview',)
    fields = ('image', 'image_preview', 'description')

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="200" height="200" style="object-fit: cover;" />',
                obj.image.url
            )
        return ""
    image_preview.short_description = "Превью"


class PatientAdmin(admin.ModelAdmin):
    inlines = [PatientImageInline]
    list_display = (
        'full_name',
        'phone',
        'avatar_preview',
        'birth_date',
        'start_treatment_date',
        'end_treatment_date'
    )
    readonly_fields = ('avatar_preview',)

    def avatar_preview(self, obj):
        """
        Возвращает HTML с тэгом <img>, если у пациента есть аватар.
        """
        if obj.avatar:
            return format_html(
                '<img src="{}" width="200" height="200" style="object-fit: cover;"/>',
                obj.avatar.url
            )
        return ""
    avatar_preview.short_description = "Аватар (превью)"


admin.site.register(Patient, PatientAdmin)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'preferred_date', 'created_at', 'status')
    search_fields = ('name', 'phone')
    list_filter = ('status', 'preferred_date')
    readonly_fields = ('created_at',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'created_at')
    search_fields = ('title',)


@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'description')
    fields = ('title', 'description', 'image')


@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    list_display = ('title',)

