from django.db import models

from .constants import SEX_CHOICES


class Patient(models.Model):
    full_name = models.CharField(max_length=255, verbose_name="ФИО")
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, verbose_name="Пол")
    age = models.PositiveIntegerField(null=True, blank=True, verbose_name="Возраст")
    contact_info = models.CharField(max_length=255, null=True, blank=True, verbose_name="Контактная информация")
    address = models.CharField(max_length=255, null=True, blank=True, verbose_name="Адрес")
    photos = models.ImageField(upload_to='static/patient_photos/', null=True, blank=True, verbose_name="Фотографии")
    general_info = models.TextField(verbose_name="Общая информация о пациенте")
    treatment_type = models.CharField(max_length=255, null=True, blank=True, verbose_name="Тип лечения")
    treatment_status = models.CharField(
        max_length=100,
        choices=[
            ('initial_consultation', 'Первичная консультация'),
            ('treatment_started', 'Лечение начато'),
            ('treatment_completed', 'Лечение завершено')
        ],
        default='initial_consultation',
        verbose_name="Статус лечения"
    )
    start_date = models.DateField(verbose_name="Дата начала лечения")
    last_visit_date = models.DateField(verbose_name="Дата последнего визита")
    next_visit_date = models.DateField(null=True, blank=True, verbose_name="Следующий визит")
    notes = models.TextField(null=True, blank=True, verbose_name="Комментарии врача")
    cost_of_treatment = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Стоимость лечения")

    class Meta:
        verbose_name = "Пациент"
        verbose_name_plural = "Пациенты"

    def __str__(self):
        return self.full_name


class Doctor(models.Model):
    full_name = models.CharField(max_length=255)
    specialty = models.CharField(max_length=255)
    contact_info = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Врач"
        verbose_name_plural = "Врачи"

    def __str__(self):
        return self.full_name
