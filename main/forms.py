from django import forms
from .models import Patient


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['full_name', 'sex', 'age', 'contact_info', 'general_info', 'treatment_type', 'start_date', 'next_visit_date']
