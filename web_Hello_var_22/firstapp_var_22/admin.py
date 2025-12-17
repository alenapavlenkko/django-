from django.contrib import admin
from .models import Category, Order, Author, Publisher, Book, Customer, Purchase, PurchaseItem, Review

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'birth_date']
    search_fields = ['last_name', 'first_name']
    list_filter = ['birth_date']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'stock', 'available', 'created']
    list_filter = ['category', 'available', 'cover_type', 'created']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'status', 'total', 'created']
    list_filter = ['status', 'payment_method', 'created']
    search_fields = ['customer__user__username', 'customer__user__email']

admin.site.register(Publisher)
admin.site.register(Customer)
admin.site.register(PurchaseItem)
admin.site.register(Review)
admin.site.register(Order)
