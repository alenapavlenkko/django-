from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django import forms
from django.core.exceptions import ValidationError
from .models import User, Category, Book, Order, OrderItem, Review


# === ФОРМА ДЛЯ OrderItem ===
class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['book', 'quantity', 'price']
        widgets = {
            'book': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
        }

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price and price <= 0:
            raise ValidationError('Цена должна быть положительной')
        return price

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity and quantity <= 0:
            raise ValidationError('Количество должно быть положительным')
        return quantity

    def clean(self):
        cleaned_data = super().clean()
        # Автоматически заполняем цену из книги, если она не указана
        book = cleaned_data.get('book')
        price = cleaned_data.get('price')

        if book and not price:
            cleaned_data['price'] = book.price

        return cleaned_data


# === ADMIN КЛАССЫ ===
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone')

    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {'fields': ('phone', 'address', 'date_of_birth', 'avatar')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Дополнительная информация', {'fields': ('phone', 'address', 'date_of_birth')}),
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'slug', 'created')
    list_filter = ('parent',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    form = OrderItemForm  # Используем нашу форму
    extra = 1  # Показывать одну пустую форму
    min_num = 1  # Минимум один товар в заказе

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        # Устанавливаем начальное значение цены из книги
        if obj is None:  # Новый заказ
            formset.form.base_fields['price'].initial = None
        return formset

    def total_price(self, obj):
        if obj and obj.pk:
            return obj.total_price
        return '—'

    total_price.short_description = 'Общая стоимость'


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'stock', 'available', 'cover_type', 'created', 'image_preview')
    list_filter = ('category', 'available', 'cover_type', 'created')
    search_fields = ('title', 'authors', 'isbn', 'description')
    list_editable = ('price', 'stock', 'available')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created', 'updated', 'image_preview')

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'authors', 'description', 'category')
        }),
        ('Детали', {
            'fields': ('isbn', 'cover_type', 'pages', 'publication_year', 'publisher')
        }),
        ('Цена и наличие', {
            'fields': ('price', 'stock', 'available')
        }),
        ('Изображение', {
            'fields': ('image', 'image_preview')
        }),
        ('Даты', {
            'fields': ('created', 'updated')
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="150" style="object-fit: cover;" />', obj.image.url)
        return "Нет изображения"

    image_preview.short_description = 'Превью'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created', 'status', 'payment_method', 'payment_status', 'total')
    list_filter = ('status', 'payment_method', 'payment_status', 'created')
    search_fields = ('user__username', 'user__email', 'shipping_address', 'notes')
    readonly_fields = ('created', 'updated')
    inlines = [OrderItemInline]

    # Автоматически вычисляем общую сумму заказа
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Обновляем общую сумму после сохранения
        obj.total = sum(item.total_price for item in obj.items.all())
        obj.save()

    fieldsets = (
        ('Основная информация', {
            'fields': ('user', 'status')
        }),
        ('Оплата и доставка', {
            'fields': ('payment_method', 'payment_status', 'shipping_address')
        }),
        ('Финансы', {
            'fields': ('total',)
        }),
        ('Дополнительно', {
            'fields': ('notes', 'created', 'updated')
        }),
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'rating', 'approved', 'created')
    list_filter = ('rating', 'approved', 'created')
    search_fields = ('book__title', 'user__username', 'comment')
    list_editable = ('approved',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('book', 'user')