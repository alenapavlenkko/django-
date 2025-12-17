# firstapp_var_22/views.py
from pathlib import Path
import csv
from openpyxl import load_workbook
from decimal import Decimal
from datetime import datetime

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Count, Sum, Avg
from django.http import HttpResponse

from .models import Book, Order, Category, Customer, Purchase, PurchaseItem
from .forms import PurchaseForm, BuyBookForm

BASE_DIR = Path(__file__).resolve().parent
TABLICA_DIR = BASE_DIR / 'tablica'


# === Главные ===
def index(request):
    return render(request, 'index.html')


def navigator(request):
    return render(request, 'navigator.html')


def thank_you(request):
    return render(request, 'thank_you.html')


# === Книги ===
def book_list(request, page=1):
    per_page = 10
    books = Book.objects.all()
    start = (page - 1) * per_page
    end = start + per_page
    return render(request, 'book_list.html', {'books': books[start:end], 'page': page})


def book_detail(request, slug, year=None):
    book = get_object_or_404(Book, slug=slug)
    return render(request, 'book_detail.html', {'book': book, 'year': year})


# === Оформление заказа (универсальная вьюха для /buy/) ===
def buy_book(request, book_id=None):
    """
    Универсальная вьюха покупки книги.
    Если book_id передан — покупка конкретной книги,
    иначе форма для произвольного выбора книги.
    """
    book = None
    if book_id:
        book = get_object_or_404(Book, pk=book_id)

    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            quantity = data.get('quantity', 1)

            # Получаем или создаём Customer
            if request.user.is_authenticated:
                customer, _ = Customer.objects.get_or_create(user=request.user)
            else:
                customer = Customer.objects.create(
                    user=None,
                    phone=data.get('phone', ''),
                    address=data.get('shipping_address', ''),
                    date_of_birth=None
                )

            # Проверка stock
            if book and book.stock < quantity:
                form.add_error('quantity', f'Доступно только {book.stock} экземпляров')
                return render(request, 'buy_book.html', {'form': form, 'book': book})

            # Создаём Purchase
            purchase = Purchase.objects.create(
                customer=customer,
                payment_method=data.get('payment_method', 'CARD'),
                shipping_address=data.get('shipping_address', ''),
                notes=data.get('notes', ''),
                total=Decimal('0.00')
            )

            total = Decimal('0.00')
            if book:
                line_price = Decimal(book.price) * quantity
                PurchaseItem.objects.create(
                    purchase=purchase,
                    book=book,
                    quantity=quantity,
                    price=book.price
                )
                total += line_price
                # Уменьшаем stock
                book.stock -= quantity
                book.save(update_fields=['stock'])

            purchase.total = total
            purchase.save(update_fields=['total'])

            messages.success(request, f'Заказ #{purchase.id} успешно создан.')
            return redirect('purchase_success', pk=purchase.id)
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        initial = {}
        if book:
            initial['book'] = str(book.title)
            initial['quantity'] = 1
        form = PurchaseForm(initial=initial)

    return render(request, 'buy_book.html', {'form': form, 'book': book})

# === Покупка конкретной книги (URL /buy/<book_id>/) ===
def buy_book_item(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        form = BuyBookForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            qty = int(data.get('quantity', 1))
            customer, _ = Customer.objects.get_or_create(user=None, defaults={'phone': '', 'address': '', 'date_of_birth': None})
            purchase = Purchase.objects.create(
                customer=customer,
                payment_method='CARD',
                shipping_address='Адрес по умолчанию',
                total=Decimal(book.price) * qty
            )
            PurchaseItem.objects.create(purchase=purchase, book=book, quantity=qty, price=book.price)
            return redirect('purchase_success', pk=purchase.id)
    else:
        form = BuyBookForm(initial={'quantity': 1, 'title': book.title})
    return render(request, 'buy_book.html', {'form': form, 'book': book})


def purchase_success(request, pk):
    purchase = get_object_or_404(Purchase, pk=pk)
    return render(request, 'purchase_success.html', {'purchase': purchase})


# === Tables / files ===
def tablica_display(request):
    rows = []
    csv_file = TABLICA_DIR / 'books.csv'
    if csv_file.exists():
        with open(csv_file, encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=';')
            rows = [row for row in reader]
    else:
        rows = [['Файл не найден', str(csv_file)]]
    return render(request, 'tablica_display.html', {'rows': rows, 'source': 'CSV'})


def tablica_from_text(request):
    rows = []
    txt_file = TABLICA_DIR / 'books.txt'
    if txt_file.exists():
        with open(txt_file, encoding='utf-8') as f:
            rows = [line.strip().split(';') for line in f if line.strip()]
    else:
        rows = [['Файл не найден', str(txt_file)]]
    return render(request, 'tablica_display.html', {'rows': rows, 'source': 'TXT'})


def tablica_from_xlsx(request):
    rows = []
    xlsx_file = TABLICA_DIR / 'books.xlsx'
    if xlsx_file.exists():
        wb = load_workbook(xlsx_file, read_only=True)
        ws = wb.active
        rows = [list(row) for row in ws.iter_rows(values_only=True)]
    else:
        rows = [['Файл не найден', str(xlsx_file)]]
    return render(request, 'tablica_display.html', {'rows': rows, 'source': 'XLSX'})


def products_demo(request):
    # читаем все 3 файла (txt/csv/xlsx)
    txt_rows, csv_rows, xlsx_rows = [], [], []
    txt_file = TABLICA_DIR / 'books.txt'
    if txt_file.exists():
        with open(txt_file, encoding='utf-8') as f:
            txt_rows = [line.strip().split(';') for line in f if line.strip()]
    csv_file = TABLICA_DIR / 'books.csv'
    if csv_file.exists():
        with open(csv_file, encoding='utf-8') as f:
            csv_rows = [row for row in csv.reader(f, delimiter=';')]
    xlsx_file = TABLICA_DIR / 'books.xlsx'
    if xlsx_file.exists():
        wb = load_workbook(xlsx_file, read_only=True)
        ws = wb.active
        xlsx_rows = [list(row) for row in ws.iter_rows(values_only=True)]
    return render(request, 'products_demo.html', {'txt_rows': txt_rows, 'csv_rows': csv_rows, 'xlsx_rows': xlsx_rows})

def simple_data(request):
    data = {
        'number': 42,
        'text': "Пример текста",
        'flag': True,
        'float_number': 3.14,
        'none_value': None
    }
    return render(request, 'simple_data.html', data)

def redirect_old_books(request):
    return redirect('web_Hello_var_22:book_list')

def order_analysis(request):
    orders = Order.objects.all()

    # -------- ФИЛЬТРАЦИЯ --------
    category_id = request.GET.get('category')
    customer_id = request.GET.get('customer')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')

    if category_id:
        orders = orders.filter(category_id=category_id)

    if customer_id:
        orders = orders.filter(customer_id=customer_id)

    if date_from:
        orders = orders.filter(order_date__gte=date_from)

    if date_to:
        orders = orders.filter(order_date__lte=date_to)

    # -------- СОРТИРОВКА --------
    sort = request.GET.get('sort', 'order_date')
    if sort in ['order_date', '-order_date', 'total_amount', '-total_amount']:
        orders = orders.order_by(sort)

    # -------- АГРЕГАТЫ --------
    stats = orders.aggregate(
        total_count=Count('id'),
        total_sum=Sum('total_amount'),
        avg_sum=Avg('total_amount')
    )

    categories = Category.objects.all()

    context = {
        'orders': orders,
        'categories': Category.objects.all(),
        'customers': Customer.objects.all(),
        'stats': stats,
    }
    return render(request, 'order_analysis.html', context)

def export_orders(request):
    orders = Order.objects.all()

    # те же фильтры!
    category_id = request.GET.get('category')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')

    if category_id:
        orders = orders.filter(category_id=category_id)
    if date_from:
        orders = orders.filter(order_date__gte=date_from)
    if date_to:
        orders = orders.filter(order_date__lte=date_to)

    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="orders_report.csv"'},
    )

    writer = csv.writer(response)
    writer.writerow(['ID', 'Customer', 'Category', 'Order Date', 'Total Amount'])

    for o in orders:
        writer.writerow([o.id, o.customer.name, o.category.name, o.order_date, o.total_amount])

    return response