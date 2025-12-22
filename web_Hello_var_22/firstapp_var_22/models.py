from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.utils.text import slugify
from decimal import Decimal
from django.core.exceptions import ValidationError  # ДОБАВИТЬ ИМПОРТ

# 1. Пользователь (заменяет и User, и Customer)
class User(AbstractUser):
    """Расширенная модель пользователя"""
    phone = models.CharField('Телефон', max_length=30, blank=True)
    address = models.TextField('Адрес', blank=True)
    date_of_birth = models.DateField('Дата рождения', blank=True, null=True)
    avatar = models.ImageField('Аватар', upload_to='users/', blank=True, null=True)
    registration_date = models.DateTimeField('Дата регистрации', auto_now_add=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


# 2. Категория (оставляем как есть, но упрощаем)
class Category(models.Model):
    name = models.CharField('Название категории', max_length=120, unique=True)
    slug = models.SlugField('URL', max_length=140, unique=True, blank=True)
    description = models.TextField('Описание', blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                               related_name='children', verbose_name='Родительская категория')
    created = models.DateTimeField('Дата создания', auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']


# 3. Книга (основная таблица товаров)
class Book(models.Model):
    COVER_TYPES = [
        ('HARD', 'Твердая обложка'),
        ('SOFT', 'Мягкая обложка'),
        ('EBOOK', 'Электронная книга'),
    ]

    title = models.CharField('Название', max_length=200)
    slug = models.SlugField('URL', max_length=200, unique=True, blank=True)
    isbn = models.CharField('ISBN', max_length=17, blank=True)
    description = models.TextField('Описание', blank=True)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2, default=Decimal('0.00'))

    # Основные поля для работы магазина
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True,
                                 blank=True, verbose_name='Категория')
    cover_type = models.CharField('Тип обложки', max_length=10, choices=COVER_TYPES, default='SOFT')
    pages = models.PositiveIntegerField('Количество страниц', default=1)
    publication_year = models.PositiveIntegerField('Год публикации', blank=True, null=True)

    # Авторы как текстовое поле для упрощения (вместо отдельной таблицы Author)
    authors = models.CharField('Авторы', max_length=500, blank=True)

    # Инвентарь
    stock = models.PositiveIntegerField('Количество на складе', default=0)
    available = models.BooleanField('Доступно', default=True)

    # === ИЗОБРАЖЕНИЕ - КАК В СТАРОМ ПРОЕКТЕ ===
    image = models.ImageField(
        'Изображение',
        upload_to='books/',  # Тот же путь что и в старом проекте
        blank=True,
        null=True
    )

    # Добавим дополнительные поля если нужны
    publisher = models.CharField('Издательство', max_length=200, blank=True)

    # Даты
    created = models.DateTimeField('Дата создания', auto_now_add=True)
    updated = models.DateTimeField('Дата обновления', auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:200]
        super().save(*args, **kwargs)

    def clean(self):
        if self.publication_year is not None:
            try:
                pub_year = int(self.publication_year)
            except (TypeError, ValueError):
                raise ValidationError({'publication_year': 'Неверный формат года публикации.'})
            if pub_year > timezone.now().year:
                raise ValidationError({'publication_year': 'Год публикации не может быть в будущем.'})

    @property
    def image_url(self):
        """Возвращает URL изображения или заглушку"""
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return '/static/images/book-placeholder.png'  # Изменил на PNG

    @property
    def has_image(self):
        """Проверяет, есть ли у книги загруженное изображение"""
        return bool(self.image and self.image.url)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
        ordering = ['-created']
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['price']),
            models.Index(fields=['available']),
            models.Index(fields=['category']),
        ]


# 4. Заказ (объединяет Purchase и Order)
class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Ожидает обработки'),
        ('PROCESSING', 'В обработке'),
        ('SHIPPED', 'Отправлен'),
        ('DELIVERED', 'Доставлен'),
        ('CANCELLED', 'Отменен'),
    ]

    PAYMENT_METHODS = [
        ('CARD', 'Карта'),
        ('CASH', 'Наличные'),
        ('ONLINE', 'Онлайн'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='PENDING')
    payment_method = models.CharField('Способ оплаты', max_length=10, choices=PAYMENT_METHODS, default='CARD')
    payment_status = models.BooleanField('Статус оплаты', default=False)
    shipping_address = models.TextField('Адрес доставки', blank=True)
    total = models.DecimalField('Общая сумма', max_digits=12, decimal_places=2, default=Decimal('0.00'))
    notes = models.TextField('Примечания', blank=True)
    created = models.DateTimeField('Дата создания', auto_now_add=True)
    updated = models.DateTimeField('Дата обновления', auto_now=True)

    def __str__(self):
        return f"Заказ #{self.id} — {self.user.username}"

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created']


# 5. Элемент заказа (подтаблица для Order)
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ', related_name='items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='Книга')
    quantity = models.PositiveIntegerField('Количество', default=1)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2, default=Decimal('0.00'))

    def clean(self):
        if self.quantity <= 0:
            raise ValidationError({'quantity': 'Количество должно быть положительным'})
        if self.price <= 0:
            raise ValidationError({'price': 'Цена должна быть положительной'})

    @property
    def total_price(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.book.title} x {self.quantity}"

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказа'


# 6. Отзыв (добавляем как шестую таблицу)
class Review(models.Model):
    RATING_CHOICES = [(i, f"{i}") for i in range(1, 6)]

    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='Книга', related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    rating = models.PositiveSmallIntegerField('Рейтинг', choices=RATING_CHOICES, default=5)
    comment = models.TextField('Комментарий', blank=True)
    approved = models.BooleanField('Одобрено', default=False)
    created = models.DateTimeField('Дата создания', auto_now_add=True)
    updated = models.DateTimeField('Дата обновления', auto_now=True)

    def clean(self):
        if self.rating < 1 or self.rating > 5:
            raise ValidationError({'rating': 'Рейтинг должен быть от 1 до 5'})

    def __str__(self):
        return f"Отзыв на {self.book.title} от {self.user.username}"

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created']
        unique_together = ['user', 'book']  # Один отзыв на книгу от пользователя