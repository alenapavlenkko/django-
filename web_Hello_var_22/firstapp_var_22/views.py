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
    print("=" * 60)
    print("DEBUG: Функция products_demo вызвана")

    txt_rows, csv_rows, xlsx_rows = [], [], []

    # --- Проверка TXT ---
    txt_file = TABLICA_DIR / 'books.txt'
    print(f"TXT файл: {txt_file}")
    print(f"TXT существует: {txt_file.exists()}")

    if txt_file.exists():
        with open(txt_file, encoding='utf-8') as f:
            content = f.read()
            print(f"TXT содержимое: {content[:200]}...")  # первые 200 символов
            f.seek(0)  # вернуться в начало файла
            txt_rows = [line.strip().split(';') for line in f if line.strip()]
            print(f"Прочитано {len(txt_rows)} строк из TXT")
    else:
        print("ОШИБКА: TXT файл не найден!")

    # --- Проверка CSV ---
    csv_file = TABLICA_DIR / 'books.csv'
    print(f"CSV файл: {csv_file}")
    print(f"CSV существует: {csv_file.exists()}")

    if csv_file.exists():
        with open(csv_file, encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=';')
            csv_rows = [row for row in reader]
            print(f"Прочитано {len(csv_rows)} строк из CSV")
    else:
        print("ОШИБКА: CSV файл не найден!")

    # --- Проверка XLSX ---
    xlsx_file = TABLICA_DIR / 'books.xlsx'
    print(f"XLSX файл: {xlsx_file}")
    print(f"XLSX существует: {xlsx_file.exists()}")

    if xlsx_file.exists():
        try:
            wb = load_workbook(xlsx_file, read_only=True, data_only=True)
            ws = wb.active
            print(f"XLSX лист: {ws.title}")
            print(f"XLSX размеры: {ws.max_row} строк, {ws.max_column} столбцов")

            # Читаем все строки
            xlsx_rows = []
            for i, row in enumerate(ws.iter_rows(values_only=True), 1):
                xlsx_rows.append(list(row))
                if i <= 3:  # покажем первые 3 строки
                    print(f"  Строка {i}: {list(row)}")

            print(f"Прочитано {len(xlsx_rows)} строк из XLSX")
        except Exception as e:
            print(f"ОШИБКА при чтении XLSX: {e}")
    else:
        print("ОШИБКА: XLSX файл не найден!")

    print("=" * 60)

    return render(request, 'products_demo.html', {
        'txt_rows': txt_rows,
        'csv_rows': csv_rows,
        'xlsx_rows': xlsx_rows
    })
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

def analysis(request):
    return render(request, 'analysis.html')

def reviews(request):
    sample_reviews = [
        {'author': 'Иван', 'text': 'Очень хорошая книга!'},
        {'author': 'Мария', 'text': 'Доставка была быстрой, спасибо!'},
        {'author': 'Алексей', 'text': 'Большой выбор и отличное обслуживание.'},
    ]
    return render(request, 'reviews.html', {'reviews': sample_reviews})

# firstapp_var_22/views.py
from pathlib import Path
from openpyxl import load_workbook

from django.shortcuts import render

BASE_DIR = Path(__file__).resolve().parent
TABLICA_DIR = BASE_DIR / 'tablica'

def files_books(request):
    text_lines = []
    excel_books = []

    # --- Текстовый файл ---
    txt_file = TABLICA_DIR / 'books.txt'
    if txt_file.exists():
        with open(txt_file, encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    # Формат: название;автор;цена;продавец
                    parts = line.split(';')
                    if len(parts) >= 4:
                        text_lines.append(f"{parts[0]} — {parts[1]} — {parts[2]} ₽ — {parts[3]}")
    else:
        print("TXT файл не найден:", txt_file)

    # --- Excel файл ---
    xlsx_file = TABLICA_DIR / 'books.xlsx'
    if xlsx_file.exists():
        wb = load_workbook(xlsx_file, read_only=True)
        ws = wb.active
        rows = list(ws.iter_rows(values_only=True))
        if rows:
            headers = rows[0]  # первая строка как заголовки
            for row in rows[1:]:
                book_data = dict(zip(headers, row))
                # Убедимся, что ключи соответствуют шаблону
                excel_books.append({
                    'title': book_data.get('название', 'Нет названия'),
                    'author': book_data.get('автор', 'Нет автора'),
                    'price': book_data.get('цена', '0'),
                    'stock': book_data.get('продавец', 'Нет информации'),
                    'image_url': book_data.get('image_url', None),  # если есть изображения
                })
    else:
        print("XLSX файл не найден:", xlsx_file)

    context = {
        'text_lines': text_lines,
        'excel_books': excel_books,
    }
    return render(request, 'products_demo.html', context)

