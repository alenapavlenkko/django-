from django.db import models
from decimal import Decimal
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.text import slugify
import os

# --- Справочники / reference tables ---
class Category(models.Model):
    name = models.CharField('Название категории', max_length=120, unique=True)
    slug = models.SlugField('URL', max_length=140, unique=True, blank=True)
    description = models.TextField('Описание', blank=True)
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


class Author(models.Model):
    first_name = models.CharField('Имя', max_length=100)
    last_name = models.CharField('Фамилия', max_length=100)
    bio = models.TextField('Биография', blank=True)
    photo = models.ImageField('Фото автора', upload_to='authors/', blank=True, null=True)
    birth_date = models.DateField('Дата рождения', blank=True, null=True)

    def clean(self):
        if self.birth_date and self.birth_date > timezone.now().date():
            raise ValidationError({'birth_date': 'Дата рождения не может быть в будущем'})

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
        ordering = ['last_name', 'first_name']


class Publisher(models.Model):
    name = models.CharField('Название', max_length=200, unique=True)
    address = models.TextField('Адрес', blank=True)
    phone = models.CharField('Телефон', max_length=30, blank=True)
    email = models.EmailField('Email', blank=True)
    website = models.URLField('Веб-сайт', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Издательство'
        verbose_name_plural = 'Издательства'
        ordering = ['name']

# --- Основные сущности (главная таблица: Book) ---
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
    cover_type = models.CharField('Тип обложки', max_length=10, choices=COVER_TYPES, default='SOFT')
    pages = models.PositiveIntegerField('Количество страниц', default=1)
    publication_year = models.PositiveIntegerField('Год публикации', blank=True, null=True)
    stock = models.PositiveIntegerField('Количество на складе', default=0)
    available = models.BooleanField('Доступно', default=True)
    image = models.ImageField('Изображение', upload_to='books/', blank=True, null=True)
    created = models.DateTimeField('Дата создания', auto_now_add=True)
    updated = models.DateTimeField('Дата обновления', auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория', null=True, blank=True)
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Издательство')
    authors = models.ManyToManyField(Author, through='BookAuthor', verbose_name='Авторы', blank=True)

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
        ]

class BookAuthor(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='ba_book')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='ba_author')

    class Meta:
        verbose_name = 'Автор книги (связь)'
        verbose_name_plural = 'Авторы книг'
        unique_together = ('book', 'author')

    def __str__(self):
        return f"{self.book.title} — {self.author}"


# --- Клиенты и профили (пример связи 1 к 1) ---

class Customer(models.Model):
    """
    Клиент — опционально связан с Django User (OneToOne).
    user nullable=True, чтобы разрешить анонимные/гостевые заказы в тестах.
    """
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Пользователь')
    phone = models.CharField('Телефон', max_length=30, blank=True)
    address = models.TextField('Адрес', blank=True)
    date_of_birth = models.DateField('Дата рождения', blank=True, null=True)
    avatar = models.ImageField('Аватар', upload_to='customers/', blank=True, null=True)
    registration_date = models.DateTimeField('Дата регистрации', auto_now_add=True)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def clean(self):
        if self.date_of_birth and self.date_of_birth > timezone.now().date():
            raise ValidationError({'date_of_birth': 'Дата рождения не может быть в будущем'})

    def __str__(self):
        if self.user:
            return self.user.get_username()
        return f"Client #{self.pk}"


# Пример связи 1-1 между Book и BookDetail (можно использовать для задачи с PostgreSQL 1:1)
class BookDetail(models.Model):
    book = models.OneToOneField(Book, on_delete=models.CASCADE, related_name='detail', verbose_name='Книга')
    language = models.CharField('Язык', max_length=50, blank=True)
    dimensions = models.CharField('Размеры', max_length=100, blank=True)
    weight = models.CharField('Вес', max_length=50, blank=True)
    created = models.DateTimeField('Создан', auto_now_add=True)

    class Meta:
        verbose_name = 'Детали книги'
        verbose_name_plural = 'Детали книг'

    def __str__(self):
        return f"Детали {self.book.title}"


# --- Заказы и позиции заказа (1 ко многим и агрегация) ---

class Purchase(models.Model):
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

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Клиент')
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='PENDING')
    payment_method = models.CharField('Способ оплаты', max_length=10, choices=PAYMENT_METHODS, default='CARD')
    payment_status = models.BooleanField('Статус оплаты', default=False)
    shipping_address = models.TextField('Адрес доставки', blank=True)
    total = models.DecimalField('Общая сумма', max_digits=12, decimal_places=2, default=Decimal('0.00'))
    notes = models.TextField('Примечания', blank=True)
    created = models.DateTimeField('Дата создания', auto_now_add=True)
    updated = models.DateTimeField('Дата обновления', auto_now=True)

    def __str__(self):
        return f"Заказ #{self.id} — {self.customer}"

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created']


class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, verbose_name='Заказ', related_name='items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='Книга')
    quantity = models.PositiveIntegerField('Количество', default=1)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2, default=Decimal('0.00'))

    def clean(self):
        if self.quantity <= 0:
            raise ValidationError({'quantity': 'Количество должно быть положительным'})
        if self.price <= 0:
            raise ValidationError({'price': 'Цена должна быть положительной'})

    def total_price(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.book.title} x {self.quantity}"

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказа'


class Review(models.Model):
    RATING_CHOICES = [(i, f"{i}") for i in range(1, 6)]

    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='Книга')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Клиент')
    rating = models.PositiveSmallIntegerField('Рейтинг', choices=RATING_CHOICES, default=5)
    title = models.CharField('Заголовок', max_length=200, blank=True)
    comment = models.TextField('Комментарий', blank=True)
    approved = models.BooleanField('Одобрено', default=False)
    created = models.DateTimeField('Дата создания', auto_now_add=True)
    updated = models.DateTimeField('Дата обновления', auto_now=True)

    def clean(self):
        if self.rating < 1 or self.rating > 5:
            raise ValidationError({'rating': 'Рейтинг должен быть от 1 до 5'})

    def __str__(self):
        return f"Отзыв на {self.book.title} от {self.customer}"

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created']


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    order_date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order #{self.id} ({self.customer})"