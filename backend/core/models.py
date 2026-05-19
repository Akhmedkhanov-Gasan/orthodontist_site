from django.db import models
from django.utils import timezone
from filer.fields.image import FilerImageField


class Service(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание", blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена", null=True, blank=True)
    image = FilerImageField(
        null=True,
        blank=True,
        related_name="service_images",
        on_delete=models.SET_NULL,
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
    patient = models.ForeignKey(
        "Patient",
        on_delete=models.SET_NULL,
        related_name="appointments",
        blank=True,
        null=True,
        verbose_name="Пациент",
    )
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
    image = FilerImageField(
        null=True,
        blank=True,
        related_name="work_images",
        on_delete=models.SET_NULL,
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
    image = FilerImageField(
        null=True,
        blank=True,
        related_name="about_page_images",
        on_delete=models.SET_NULL,
        verbose_name="Картинка"
    )
    value_1_title = models.CharField(
        max_length=200,
        verbose_name="Ценность 1 - заголовок",
        blank=True,
        default="Профессионализм",
    )
    value_1_description = models.TextField(
        verbose_name="Ценность 1 - описание",
        blank=True,
        default="Постоянное совершенствование навыков и применение передовых методик",
    )

    value_2_title = models.CharField(
        max_length=200,
        verbose_name="Ценность 2 - заголовок",
        blank=True,
        default="Инновации",
    )
    value_2_description = models.TextField(
        verbose_name="Ценность 2 - описание",
        blank=True,
        default="Использование современного оборудования и цифровых технологий",
    )

    value_3_title = models.CharField(
        max_length=200,
        verbose_name="Ценность 3 - заголовок",
        blank=True,
        default="Забота",
    )
    value_3_description = models.TextField(
        verbose_name="Ценность 3 - описание",
        blank=True,
        default="Индивидуальный подход и внимание к каждому пациенту",
    )

    team_title = models.CharField(
        max_length=200,
        verbose_name="Команда - заголовок",
        blank=True,
        default="Наша команда",
    )
    team_text = models.TextField(
        verbose_name="Команда - текст",
        blank=True,
        default="Наши специалисты регулярно проходят обучение и стажировки в ведущих клиниках мира, чтобы предоставлять вам лечение на высочайшем уровне.",
    )

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "О нас (редактирование)"

    def save(self, *args, **kwargs):
        if not self.pk and AboutPage.objects.exists():
            raise ValueError("Можно создать только одну страницу О нас")

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "О нас"
        verbose_name_plural = "О нас"


class Patient(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый пациент'),
        ('in_progress', 'В процессе'),
        ('completed', 'Лечение окончено'),
    ]
    avatar = FilerImageField(
        null=True,
        blank=True,
        related_name="patient_avatars",
        on_delete=models.SET_NULL,
        verbose_name="Аватар"
    )
    full_name = models.CharField(max_length=100, verbose_name="ФИО")
    phone = models.CharField(
        max_length=30,
        verbose_name="Телефон",
        blank=True, null=True
    )
    telegram_id = models.BigIntegerField(
        unique=True,
        blank=True,
        null=True,
        verbose_name="Telegram ID",
    )
    telegram_username = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name="Telegram username",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен",
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
    image = FilerImageField(
        verbose_name="Изображение",
        on_delete=models.CASCADE
    )
    description = models.CharField(max_length=255, blank=True, verbose_name="Описание")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "дополнительное изображение"
        verbose_name_plural = "дополнительные изображения"

    def __str__(self):
        return f"Image for {self.patient.full_name}"


class HomePage(models.Model):
    hero_title = models.CharField(
        max_length=200,
        verbose_name="Заголовок главного блока"
    )
    hero_subtitle = models.TextField(
        verbose_name="Описание главного блока",
        blank=True
    )
    hero_button_text = models.CharField(
        max_length=100,
        verbose_name="Текст кнопки",
        default="Записаться на консультацию"
    )
    hero_button_url = models.CharField(
        max_length=200,
        verbose_name="Ссылка кнопки",
        default="/appointment"
    )
    hero_image = FilerImageField(
        null=True,
        blank=True,
        related_name="home_hero_images",
        on_delete=models.SET_NULL,
        verbose_name="Картинка главного блока"
    )

    about_title = models.CharField(
        max_length=200,
        verbose_name="Заголовок блока о клинике",
        blank=True
    )
    about_text = models.TextField(
        verbose_name="Текст блока о клинике",
        blank=True
    )

    feature_1_title = models.CharField(
        max_length=200,
        verbose_name="Преимущество 1 - заголовок",
        default="3D-планирование лечения"
    )
    feature_1_description = models.TextField(
        verbose_name="Преимущество 1 - описание",
        default="Используем современные технологии для визуализации результатов до начала лечения"
    )

    feature_2_title = models.CharField(
        max_length=200,
        verbose_name="Преимущество 2 - заголовок",
        default="Цифровые оттиски"
    )
    feature_2_description = models.TextField(
        verbose_name="Преимущество 2 - описание",
        default="Забудьте о неприятных процедурах. Используем только цифровые сканеры"
    )

    feature_3_title = models.CharField(
        max_length=200,
        verbose_name="Преимущество 3 - заголовок",
        default="Виртуальная консультация"
    )
    feature_3_description = models.TextField(
        verbose_name="Преимущество 3 - описание",
        default="Первичная консультация возможна онлайн. Экономьте своё время"
    )

    about_bullet_1 = models.CharField(
        max_length=255,
        verbose_name="Пункт 1",
        default="Команда высококвалифицированных специалистов"
    )
    about_bullet_2 = models.CharField(
        max_length=255,
        verbose_name="Пункт 2",
        default="Индивидуальный подход к каждому пациенту"
    )
    about_bullet_3 = models.CharField(
        max_length=255,
        verbose_name="Пункт 3",
        default="Использование современного оборудования"
    )
    about_bullet_4 = models.CharField(
        max_length=255,
        verbose_name="Пункт 4",
        default="Комфортные условия лечения"
    )

    footer_title = models.CharField(
        max_length=100,
        verbose_name="Название в футере",
        default="JML ORTHO"
    )
    footer_description = models.CharField(
        max_length=255,
        verbose_name="Описание в футере",
        default="Профессиональная ортодонтическая клиника"
    )
    footer_copyright = models.CharField(
        max_length=255,
        verbose_name="Копирайт",
        default="© 2025 JML ORTHO. Все права защищены."
    )
    footer_contacts = models.CharField(
        max_length=255,
        verbose_name="Адрес и телефон",
        default="г. Москва, ул. Примерная, д. 1 | Тел: +7 (495) 123-45-67"
    )
    telegram_url = models.URLField(
        max_length=255,
        verbose_name="Ссылка на Telegram",
        blank=True,
        default=""
    )
    instagram_url = models.URLField(
        max_length=255,
        verbose_name="Ссылка на Instagram",
        blank=True,
        default=""
    )

    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk and HomePage.objects.exists():
            raise ValueError("Можно создать только одну главную страницу")

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Главная страница"
        verbose_name_plural = "Главная страница"

    def __str__(self):
        return "Главная страница"

class TeamMember(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Имя"
    )
    position = models.CharField(
        max_length=200,
        verbose_name="Должность",
        blank=True
    )
    description = models.TextField(
        verbose_name="Описание",
        blank=True
    )
    photo = FilerImageField(
        null=True,
        blank=True,
        related_name="team_member_photos",
        on_delete=models.SET_NULL,
        verbose_name="Фото"
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Порядок"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Показывать на сайте"
    )
    work_start_date = models.DateField(
        verbose_name="Дата начала работы",
        blank=True,
        null=True,
    )

    @property
    def experience_years(self):
        if not self.work_start_date:
            return None

        today = timezone.localdate()
        years = today.year - self.work_start_date.year

        if (today.month, today.day) < (self.work_start_date.month, self.work_start_date.day):
            years -= 1

        return max(years, 0)

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
        ordering = ["order", "id"]

    def __str__(self):
        return self.name