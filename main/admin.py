from django.contrib import admin
from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'age', 'sex', 'start_date', 'last_visit_date', 'treatment_status', 'next_visit_date')
    search_fields = ('full_name', 'contact_info')
    list_filter = ('treatment_status', 'start_date', 'last_visit_date')

