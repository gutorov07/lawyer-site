# lawyer_site/models.py
from django.db import models
from django.core.validators import MinLengthValidator, MaxValueValidator, MinValueValidator
from django.utils import timezone
from django.contrib.auth import get_user_model
# Для расширенного текстового редактора (опционально)

from django.db.models import TextField as RichTextField

User = get_user_model()


class Service(models.Model):
    """Модель для услуг юридической компании"""
    CATEGORY_CHOICES = [
        ('corporate', 'Корпоративное право'),
        ('family', 'Семейное право'),
        ('criminal', 'Уголовное право'),
        ('civil', 'Гражданское право'),
        ('tax', 'Налоговое право'),
        ('labor', 'Трудовое право'),
        ('property', 'Недвижимость'),
        ('inheritance', 'Наследственное право'),
        ('other', 'Другое'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='Название услуги')
    short_description = models.CharField(max_length=300, verbose_name='Краткое описание', blank=True)
    full_description = models.TextField(verbose_name='Полное описание', blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other', verbose_name='Категория')
    
    price_from = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена от', blank=True, null=True)
    price_to = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена до', blank=True, null=True)
    duration = models.CharField(max_length=100, verbose_name='Сроки выполнения', blank=True)
    
    icon = models.CharField(max_length=100, verbose_name='Иконка', default='bi-briefcase', blank=True)
    image = models.ImageField(upload_to='services/', verbose_name='Изображение', blank=True, null=True)
    
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок отображения')
    is_active = models.BooleanField(default=True, verbose_name='Активна')
    is_featured = models.BooleanField(default=False, verbose_name='Рекомендуемая услуга')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
        ordering = ['order', 'title']
    
    def __str__(self):
        return self.title
    
    def get_price_display(self):
        if self.price_from and self.price_to:
            return f"от {self.price_from} до {self.price_to} руб."
        elif self.price_from:
            return f"от {self.price_from} руб."
        elif self.price_to:
            return f"до {self.price_to} руб."
        return "Цена по запросу"
    

    class Service(models.Model):
        SERVICE_TYPES = [
        ('consumer', 'Защита прав потребителя'),
        ('family', 'Семейное право'),
        ('auto', 'Автоюрист'),
        ('compensation', 'Возмещение вреда'),
        ('debt', 'Взыскание долгов'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='Название услуги')
    service_type = models.CharField(
    max_length=50, 
    verbose_name='Тип услуги',
    help_text='Например: потребитель, семейное, авто и т.д.'
    )
    short_description = models.TextField(verbose_name='Краткое описание')
    full_description = models.TextField(verbose_name='Полное описание')
    price_from = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена от')
    price_to = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Цена до')
    icon = models.CharField(max_length=50, default='bi-briefcase', verbose_name='Иконка')
    is_active = models.BooleanField(default=True, verbose_name='Активна')
    order = models.IntegerField(default=0, verbose_name='Порядок')
    
    def get_price_display(self):
        if self.price_to:
            return f"от {self.price_from} до {self.price_to} ₽"
        return f"от {self.price_from} ₽"
    
    class Meta:
        ordering = ['order', 'title']
    
    def __str__(self):
        return self.title

class LawyerInfo(models.Model):
    """Модель для информации о юристах"""
    POSITION_CHOICES = [
        ('lawyer', 'Юрист'),
        ('senior_lawyer', 'Старший юрист'),
        ('leading_lawyer', 'Ведущий юрист'),
        ('partner', 'Партнер'),
        ('senior_partner', 'Старший партнер'),
        ('head', 'Руководитель направления'),
    ]
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='lawyer_profile',
        verbose_name='Пользователь',
        blank=True,
        null=True
    )
    first_name = models.CharField(
        max_length=100,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=100,
        verbose_name='Фамилия'
    )
    middle_name = models.CharField(
        max_length=100,
        verbose_name='Отчество',
        blank=True
    )
    
    position = models.CharField(
        max_length=50,
        choices=POSITION_CHOICES,
        default='lawyer',
        verbose_name='Должность'
    )
    specialization = models.CharField(
        max_length=200,
        verbose_name='Специализация'
    )
    bio = RichTextField(
        verbose_name='Биография',
        help_text='Подробная информация о юристе'
    )
    experience_years = models.PositiveIntegerField(
        verbose_name='Стаж работы (лет)',
        default=0
    )
    education = models.TextField(
        verbose_name='Образование'
    )
    
    email = models.EmailField(
        verbose_name='Email',
        unique=True
    )
    phone = models.CharField(
        max_length=20,
        verbose_name='Телефон',
        help_text='Формат: +7 XXX XXX-XX-XX'
    )
    office = models.CharField(
        max_length=100,
        verbose_name='Кабинет',
        blank=True
    )
    
    photo = models.ImageField(
        upload_to='lawyers/',
        verbose_name='Фотография',
        blank=True,
        null=True
    )
    services = models.ManyToManyField(
        Service,
        related_name='lawyers',
        verbose_name='Услуги',
        blank=True
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активен'
    )
    is_featured = models.BooleanField(
        default=False,
        verbose_name='Показать на главной'
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок отображения'
    )
    
    vk_link = models.URLField(
        verbose_name='Ссылка на VK',
        blank=True
    )
    telegram_link = models.URLField(
        verbose_name='Ссылка на Telegram',
        blank=True
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )
    
    class Meta:
        verbose_name = 'Юрист'
        verbose_name_plural = 'Юристы'
        ordering = ['order', 'last_name', 'first_name']
        indexes = [
            models.Index(fields=['is_active', 'is_featured']),
            models.Index(fields=['position', 'experience_years']),
        ]
    
    def __str__(self):
        return f"{self.last_name} {self.first_name}"
    
    def full_name(self):
        """Полное ФИО"""
        if self.middle_name:
            return f"{self.last_name} {self.first_name} {self.middle_name}"
        return f"{self.last_name} {self.first_name}"
    
    def get_experience_display(self):
        """Форматированное отображение стажа"""
        years = self.experience_years
        if years == 1:
            return "1 год"
        elif 2 <= years <= 4:
            return f"{years} года"
        else:
            return f"{years} лет"


class Case(models.Model):
    """Модель для успешных дел/кейсов"""
    STATUS_CHOICES = [
        ('completed', 'Завершено успешно'),
        ('in_progress', 'В процессе'),
        ('pending', 'Ожидает рассмотрения'),
    ]
    
    title = models.CharField(
        max_length=200,
        verbose_name='Название дела'
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='URL-адрес'
    )
    
    client = models.CharField(
        max_length=200,
        verbose_name='Клиент',
        help_text='Имя или организация клиента'
    )
    description = RichTextField(
        verbose_name='Описание ситуации'
    )
    challenge = RichTextField(
        verbose_name='Проблема/Задача',
        help_text='С какими трудностями столкнулись'
    )
    solution = RichTextField(
        verbose_name='Решение'
    )
    result = RichTextField(
        verbose_name='Результат'
    )
    
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='cases',
        verbose_name='Услуга'
    )
    lawyers = models.ManyToManyField(
        LawyerInfo,
        related_name='cases',
        verbose_name='Юристы'
    )
    
    case_date = models.DateField(
        verbose_name='Дата завершения дела',
        default=timezone.now
    )
    duration_months = models.PositiveIntegerField(
        verbose_name='Продолжительность (месяцев)',
        default=1
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='completed',
        verbose_name='Статус'
    )
    complexity = models.PositiveIntegerField(
        verbose_name='Сложность дела (1-10)',
        default=5,
        validators=[MaxValueValidator(10), MinValueValidator(1)]
    )
    
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано'
    )
    is_featured = models.BooleanField(
        default=False,
        verbose_name='Показать на главной'
    )
    
    image = models.ImageField(
        upload_to='cases/',
        verbose_name='Изображение',
        blank=True,
        null=True
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )
    
    class Meta:
        verbose_name = 'Дело/Кейс'
        verbose_name_plural = 'Дела/Кейсы'
        ordering = ['-case_date', '-created_at']
        indexes = [
            models.Index(fields=['status', 'is_published']),
            models.Index(fields=['service', 'case_date']),
        ]
    
    def __str__(self):
        return self.title


class Certificate(models.Model):
    """Модель для сертификатов и дипломов юристов"""
    lawyer = models.ForeignKey(
        LawyerInfo,
        on_delete=models.CASCADE,
        related_name='certificates',
        verbose_name='Юрист'
    )
    
    title = models.CharField(
        max_length=200,
        verbose_name='Название сертификата'
    )
    issuer = models.CharField(
        max_length=200,
        verbose_name='Организация-выдаватель'
    )
    issue_date = models.DateField(
        verbose_name='Дата выдачи'
    )
    expiry_date = models.DateField(
        verbose_name='Дата окончания действия',
        blank=True,
        null=True
    )
    
    certificate_number = models.CharField(
        max_length=100,
        verbose_name='Номер сертификата',
        blank=True
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True
    )
    
    file = models.FileField(
        upload_to='certificates/',
        verbose_name='Файл сертификата',
        blank=True,
        null=True
    )
    image = models.ImageField(
        upload_to='certificates/images/',
        verbose_name='Изображение сертификата',
        blank=True,
        null=True
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активен'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    
    class Meta:
        verbose_name = 'Сертификат'
        verbose_name_plural = 'Сертификаты'
        ordering = ['-issue_date']
    
    def __str__(self):
        return f"{self.title} - {self.lawyer}"
    
    def is_valid(self):
        """Проверка действительности сертификата"""
        if not self.expiry_date:
            return True
        return self.expiry_date >= timezone.now().date()


class Article(models.Model):
    """Модель для статей блога"""
    CATEGORY_CHOICES = [
        ('news', 'Новости'),
        ('analytics', 'Аналитика'),
        ('tips', 'Советы'),
        ('legislation', 'Законодательство'),
        ('practice', 'Судебная практика'),
    ]
    
    title = models.CharField(
        max_length=200,
        verbose_name='Заголовок'
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='URL-адрес'
    )
    
    author = models.ForeignKey(
        LawyerInfo,
        on_delete=models.CASCADE,
        related_name='articles',
        verbose_name='Автор'
    )
    
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='news',
        verbose_name='Категория'
    )
    
    excerpt = models.CharField(
        max_length=300,
        verbose_name='Краткое описание',
        help_text='Отображается в списке статей'
    )
    content = RichTextField(
        verbose_name='Содержание'
    )
    
    image = models.ImageField(
        upload_to='articles/',
        verbose_name='Главное изображение',
        blank=True,
        null=True
    )
    thumbnail = models.ImageField(
        upload_to='articles/thumbnails/',
        verbose_name='Миниатюра',
        blank=True,
        null=True
    )
    
    tags = models.CharField(
        max_length=200,
        verbose_name='Теги',
        blank=True,
        help_text='Через запятую'
    )
    
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано'
    )
    is_featured = models.BooleanField(
        default=False,
        verbose_name='Рекомендуемая статья'
    )
    allow_comments = models.BooleanField(
        default=True,
        verbose_name='Разрешить комментарии'
    )
    
    views_count = models.PositiveIntegerField(
        default=0,
        verbose_name='Количество просмотров'
    )
    reading_time = models.PositiveIntegerField(
        default=5,
        verbose_name='Время чтения (минут)'
    )
    
    published_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='Дата публикации'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )
    
    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-published_at', '-created_at']
        indexes = [
            models.Index(fields=['is_published', 'category']),
            models.Index(fields=['author', 'published_at']),
        ]
    
    def __str__(self):
        return self.title
    
    def increment_views(self):
        """Увеличить счетчик просмотров"""
        self.views_count += 1
        self.save(update_fields=['views_count'])


class ContactRequest(models.Model):
    """Модель для заявок с формы обратной связи"""
    REQUEST_TYPE_CHOICES = [
        ('consultation', 'Консультация'),
        ('service', 'Заказ услуги'),
        ('callback', 'Обратный звонок'),
        ('complaint', 'Жалоба'),
        ('other', 'Другое'),
    ]
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in_progress', 'В обработке'),
        ('completed', 'Завершена'),
        ('rejected', 'Отклонена'),
    ]
    
    name = models.CharField(
        max_length=100,
        verbose_name='Имя'
    )
    phone = models.CharField(
        max_length=20,
        verbose_name='Телефон'
    )
    email = models.EmailField(
        verbose_name='Email',
        blank=True
    )
    
    request_type = models.CharField(
        max_length=20,
        choices=REQUEST_TYPE_CHOICES,
        default='consultation',
        verbose_name='Тип запроса'
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Услуга'
    )
    lawyer = models.ForeignKey(
        LawyerInfo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Предпочтительный юрист'
    )
    
    message = models.TextField(
        verbose_name='Сообщение',
        blank=True
    )
    
    ip_address = models.GenericIPAddressField(
        verbose_name='IP адрес',
        blank=True,
        null=True
    )
    user_agent = models.TextField(
        verbose_name='User Agent',
        blank=True
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name='Статус'
    )
    is_processed = models.BooleanField(
        default=False,
        verbose_name='Обработано'
    )
    
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Ответственный'
    )
    notes = models.TextField(
        verbose_name='Заметки менеджера',
        blank=True
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    processed_at = models.DateTimeField(
        verbose_name='Дата обработки',
        blank=True,
        null=True
    )
    
    class Meta:
        verbose_name = 'Запрос с формы'
        verbose_name_plural = 'Запросы с формы'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'is_processed']),
            models.Index(fields=['request_type', 'created_at']),
        ]
    
    def __str__(self):
        return f"Запрос от {self.name} ({self.get_request_type_display()})"
    
    def mark_as_processed(self, user=None, notes=''):
        """Пометить запрос как обработанный"""
        self.is_processed = True
        self.status = 'completed'
        self.assigned_to = user
        self.notes = notes
        self.processed_at = timezone.now()
        self.save()


class FAQ(models.Model):
    """Модель для часто задаваемых вопросов"""
    CATEGORY_CHOICES = [
        ('general', 'Общие вопросы'),
        ('services', 'Вопросы об услугах'),
        ('prices', 'Цены и оплата'),
        ('process', 'Процесс работы'),
        ('documents', 'Документы'),
        ('other', 'Другое'),
    ]
    
    question = models.CharField(
        max_length=300,
        verbose_name='Вопрос'
    )
    answer = RichTextField(
        verbose_name='Ответ'
    )
    
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='general',
        verbose_name='Категория'
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок отображения'
    )
    
    service = models.ForeignKey(
        Service,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='faqs',
        verbose_name='Связанная услуга'
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активен'
    )
    is_general = models.BooleanField(
        default=False,
        verbose_name='Общий вопрос',
        help_text='Будет отображаться на главной странице FAQ'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )
    
    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQ'
        ordering = ['category', 'order', 'question']
        indexes = [
            models.Index(fields=['category', 'is_active']),
            models.Index(fields=['is_general', 'order']),
        ]
    
    def __str__(self):
        return self.question[:100]