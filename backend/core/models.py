from django.db import models


class Service(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание", blank=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена",
        null=True,
        blank=True
    )
    image = models.ImageField(
        upload_to='services/',
        blank=True,
        null=True,
        verbose_name="Изображение"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Услугу"
        verbose_name_plural = "Услуги"

    def __str__(self):
        return self.title


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая запись'),
        ('repeat', 'Повторная запись'),
        ('confirmed', 'Подтверждено'),
        ('done', 'Завершено'),
        ('canceled', 'Отменено'),
    ]

    name = models.CharField(max_length=100, verbose_name="Имя")
    phone = models.CharField(max_length=30, verbose_name="Телефон")
    message = models.TextField(verbose_name="Комментарий", blank=True)
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания записи"
    )
    preferred_date = models.DateField(
        verbose_name="Предпочтительная дата",
        blank=True,
        null=True
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name="Статус"
    )

    class Meta:
        verbose_name = "Запись на приём"
        verbose_name_plural = "Записи на приём"

    def __str__(self):
        return f"{self.name} - {self.phone}"


class Work(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название работы")
    description = models.TextField(verbose_name="Описание", blank=True)
    image = models.ImageField(
        upload_to='works/',
        blank=True,
        null=True,
        verbose_name="Картинка"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Наши работы"
        verbose_name_plural = "Наши работы"

    def __str__(self):
        return self.title


class AboutPage(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Основной текст")
    image = models.ImageField(
        upload_to='about/',
        blank=True,
        null=True,
        verbose_name="Картинка"
    )

    def __str__(self):
        return "О нас (редактирование)"

    class Meta:
        verbose_name = "О нас"
        verbose_name_plural = "О нас"


class Patient(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый пациент'),
        ('in_progress', 'В процессе'),
        ('completed', 'Лечение окончено'),
    ]

    full_name = models.CharField(max_length=100, verbose_name="ФИО")
    phone = models.CharField(
        max_length=30,
        verbose_name="Телефон",
        blank=True, null=True
    )
    email = models.EmailField(
        verbose_name="Email",
        blank=True,
        null=True
    )
    birth_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="Дата рождения"
    )
    start_treatment_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="Дата начала лечения"
    )
    end_treatment_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="Дата окончания лечения"
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание"
    )
    initial_service_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Стартовая стоимость услуг"
    )
    amount_paid = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Оплачено"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name="Статус"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    avatar = models.ImageField(
        upload_to='patients/avatars/',
        blank=True,
        null=True,
        verbose_name="Аватар"
    )

    class Meta:
        verbose_name = "Пациент"
        verbose_name_plural = "Пациенты"

    def __str__(self):
        return self.full_name



class PatientImage(models.Model):
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(
        upload_to='patients/',
        verbose_name="Изображение"
    )
    description = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Описание"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "дополнительное изображение"
        verbose_name_plural = "дополнительные изображения"

    def __str__(self):
        return f"Image for {self.patient.full_name}"
