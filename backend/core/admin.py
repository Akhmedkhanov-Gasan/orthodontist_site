from django.contrib import admin
from django.utils.html import format_html
from django.shortcuts import redirect
from django.urls import reverse

from .models import (
    Patient, PatientImage,
    Appointment,
    Service,
    Work,
    AboutPage,
    HomePage,
)


class PatientImageInline(admin.TabularInline):
    model = PatientImage


class PatientAdmin(admin.ModelAdmin):
    inlines = [PatientImageInline]
    list_display = (
        'avatar_preview',
        'full_name',
        'phone',
        'birth_date',
        'start_treatment_date',
        'end_treatment_date',
        'status',
        'initial_service_cost',
        'amount_paid',
        'telegram_username',
        'telegram_id',
        'is_active',
    )
    search_fields = ('full_name', 'phone', 'telegram_username', 'telegram_id')
    list_filter = ('status', 'is_active')

    def avatar_preview(self, obj):
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
    list_display = ('name', 'phone', 'patient', 'preferred_date', 'created_at', 'status')
    search_fields = (
        'name',
        'phone',
        'patient__full_name',
        'patient__phone',
        'patient__telegram_username',
    )
    list_filter = ('status', 'preferred_date', 'created_at')
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


@admin.register(HomePage)
class HomePageAdmin(admin.ModelAdmin):
    list_display = ("hero_title", "updated_at")

    fieldsets = (
        ("Главный блок", {
            "fields": (
                "hero_title",
                "hero_subtitle",
                "hero_button_text",
                "hero_button_url",
                "hero_image",
            )
        }),
        ("Преимущества", {
            "fields": (
                "feature_1_title",
                "feature_1_description",
                "feature_2_title",
                "feature_2_description",
                "feature_3_title",
                "feature_3_description",
            )
        }),
        ("Блок о клинике", {
            "fields": (
                "about_title",
                "about_text",
                "about_bullet_1",
                "about_bullet_2",
                "about_bullet_3",
                "about_bullet_4",
            )
        }),
        ("Футер", {
            "fields": (
                "footer_title",
                "footer_description",
                "footer_copyright",
                "footer_contacts",
                "telegram_url",
                "instagram_url",
            )
        }),
    )

    def has_add_permission(self, request):
        if HomePage.objects.exists():
            return False

        return super().has_add_permission(request)

    def changelist_view(self, request, extra_context=None):
        home_page = HomePage.objects.first()

        if home_page:
            url = reverse(
                "admin:core_homepage_change",
                args=[home_page.pk],
            )
            return redirect(url)

        return super().changelist_view(request, extra_context)
