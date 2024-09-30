from django.contrib import admin
from django.utils.html import format_html
from main.models import Patient, Doctor
from django.utils.translation import gettext_lazy as _


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'age', 'sex', 'start_date', 'last_visit_date', 'treatment_status', 'next_visit_date', 'photo_preview')
    search_fields = ('full_name', 'contact_info')
    list_filter = ('treatment_status', 'start_date', 'last_visit_date')
    date_hierarchy = 'start_date'
    actions = ['mark_treatment_completed', 'delete_selected_patients']

    fieldsets = (
        ('Персональная информация', {
            'fields': (
            'full_name', 'sex', 'age', 'contact_info', 'address', 'photos')
        }),
        ('Информация о лечении', {
            'fields': ('treatment_type', 'treatment_status', 'start_date',
                       'last_visit_date', 'next_visit_date',
                       'cost_of_treatment')
        }),
        ('Заметки', {
            'fields': ('general_info', 'notes')
        }),
    )

    def photo_preview(self, obj):
        if obj.photos:
            return format_html(
                '<a href="{}" target="_blank"><img src="{}" style="width: 50px; height:50px;" /></a>',
                obj.photos.url,
                obj.photos.url
            )
        return "No Image"
    photo_preview.short_description = 'Photo Preview'

    @admin.action(description='Завершить лечение у всех выделенных пациентов')
    def mark_treatment_completed(self, request, queryset):
        queryset.update(treatment_status='treatment_completed')

    @admin.action(description='Удалить всех выделенных пациентов')
    def delete_selected_patients(self, request, queryset):
        count = queryset.count()
        queryset.delete()
        self.message_user(request,
                          _("{} пациенты успешно удалены.").format(count))

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'specialty', 'contact_info')
    search_fields = ('full_name', 'specialty')
