from django.contrib import admin
from django.utils.html import format_html
from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'age', 'sex', 'start_date', 'last_visit_date', 'treatment_status', 'next_visit_date', 'photo_preview')
    search_fields = ('full_name', 'contact_info')
    list_filter = ('treatment_status', 'start_date', 'last_visit_date')
    date_hierarchy = 'start_date'
    actions = ['mark_treatment_completed']

    fieldsets = (
        ('Personal Info', {
            'fields': ('full_name', 'sex', 'age', 'contact_info', 'address', 'photos')
        }),
        ('Treatment Info', {
            'fields': ('treatment_type', 'treatment_status', 'start_date', 'last_visit_date', 'next_visit_date', 'cost_of_treatment')
        }),
        ('Notes', {
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

    @admin.action(description='Mark selected treatments as completed')
    def mark_treatment_completed(self, request, queryset):
        queryset.update(treatment_status='treatment_completed')
