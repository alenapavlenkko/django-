# firstapp_var_22/tests.py
from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from decimal import Decimal
from .models import Book, Category, Author, Customer, Purchase, PurchaseItem

class BookModelTest(TestCase):
    def setUp(self):
        self.cat = Category.objects.create(name='Программирование')
        self.book = Book.objects.create(
            title='Тестовая книга',
            isbn='1234567890',
            price=Decimal('499.00'),
            publication_year=2020,
            category=self.cat
        )

    def test_create_and_read(self):
        b = Book.objects.get(pk=self.book.pk)
        self.assertEqual(b.title, 'Тестовая книга')
        self.assertEqual(str(b), 'Тестовая книга')

    def test_update(self):
        self.book.price = Decimal('599.00')
        self.book.save()
        b = Book.objects.get(pk=self.book.pk)
        self.assertEqual(b.price, Decimal('599.00'))

    def test_delete(self):
        pk = self.book.pk
        self.book.delete()
        with self.assertRaises(Book.DoesNotExist):
            Book.objects.get(pk=pk)
