"""
Главный файл Flask приложения для аналитики книжного магазина
"""

from flask import Flask, render_template, jsonify, request, send_file, flash, redirect, url_for
import os
import csv
from datetime import datetime
from config import SECRET_KEY, get_export_path
from database import execute_query, check_database_connection

app = Flask(__name__)
app.secret_key = SECRET_KEY


# ==================== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ====================

def format_date(date_str):
    """Форматирование даты для отображения"""
    if not date_str:
        return ''
    try:
        # Пробуем разные форматы дат
        for fmt in ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d', '%Y-%m-%d %H:%M:%S.%f']:
            try:
                dt = datetime.strptime(str(date_str), fmt)
                return dt.strftime('%d.%m.%Y')
            except:
                continue
        return str(date_str)[:10]  # Возвращаем первые 10 символов
    except:
        return str(date_str)


def get_paginated_data(data, page, per_page):
    """Пагинация данных"""
    start = (page - 1) * per_page
    end = start + per_page
    return data[start:end]


# Регистрируем фильтры для Jinja2
@app.template_filter('dateformat')
def dateformat_filter(value):
    return format_date(value)


# ==================== МАРШРУТЫ ====================

# Добавьте в app.py после импортов, перед маршрутами

# Регистрируем фильтры для Jinja2
@app.template_filter('dateformat')
def dateformat_filter(value, format='%d.%m.%Y'):
    """Форматирование даты для отображения"""
    if not value:
        return ''
    try:
        if isinstance(value, str):
            # Пробуем разные форматы дат
            for fmt in ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d', '%Y-%m-%d %H:%M:%S.%f']:
                try:
                    dt = datetime.strptime(str(value), fmt)
                    return dt.strftime(format)
                except:
                    continue
            return str(value)[:10]  # Возвращаем первые 10 символов
        elif hasattr(value, 'strftime'):  # Это datetime объект
            return value.strftime(format)
        else:
            return str(value)
    except:
        return str(value)

@app.template_filter('datetimeformat')
def datetimeformat_filter(value, format='%d.%m.%Y %H:%M'):
    """Форматирование даты и времени"""
    return dateformat_filter(value, format)
@app.route('/')
def index():
    """Главная страница"""
    try:
        # Основная статистика
        stats = execute_query("""
            SELECT 
                (SELECT COUNT(*) FROM firstapp_var_22_book) as total_books,
                (SELECT COUNT(*) FROM firstapp_var_22_order) as total_orders,
                (SELECT COUNT(*) FROM firstapp_var_22_user) as total_users,
                (SELECT COALESCE(SUM(total), 0) FROM firstapp_var_22_order WHERE status = 'completed') as total_revenue
        """)[0]

        # Последние заказы
        recent_orders = execute_query("""
            SELECT o.id, o.created, o.total, u.username 
            FROM firstapp_var_22_order o
            LEFT JOIN firstapp_var_22_user u ON o.user_id = u.id
            ORDER BY o.created DESC LIMIT 5
        """)

        # Топ книг по остатку
        top_books = execute_query("""
            SELECT title, authors, price, stock 
            FROM firstapp_var_22_book 
            WHERE stock > 0 
            ORDER BY stock DESC LIMIT 5
        """)

        return render_template('index.html',
                               stats=stats,
                               recent_orders=recent_orders,
                               top_books=top_books)

    except Exception as e:
        print(f"Ошибка на главной странице: {e}")
        flash(f"Ошибка загрузки данных: {e}", "danger")
        return render_template('index.html', stats={}, recent_orders=[], top_books=[])


@app.route('/dashboard')
def dashboard():
    """Дашборд с аналитикой"""
    try:
        # Общая статистика
        stats_query = """
            SELECT 
                COUNT(DISTINCT o.id) as total_orders,
                COALESCE(SUM(o.total), 0) as total_revenue,
                COUNT(DISTINCT o.user_id) as active_customers,
                COALESCE(AVG(o.total), 0) as avg_order_value
            FROM firstapp_var_22_order o
            WHERE o.status = 'completed'
        """
        stats = execute_query(stats_query)[0]

        # Статистика за сегодня
        today = datetime.now().strftime('%Y-%m-%d')
        today_stats = execute_query("""
            SELECT 
                COUNT(*) as today_orders,
                COALESCE(SUM(total), 0) as today_revenue
            FROM firstapp_var_22_order
            WHERE DATE(created) = %s AND status = 'completed'
        """, [today])
        today_stats = today_stats[0] if today_stats else {}

        # Продажи за последние 7 дней
        weekly_sales = execute_query("""
            SELECT 
                DATE(created) as date,
                COUNT(*) as orders_count,
                COALESCE(SUM(total), 0) as daily_revenue
            FROM firstapp_var_22_order
            WHERE created >= CURRENT_DATE - INTERVAL '7 days'
                AND status = 'completed'
            GROUP BY DATE(created)
            ORDER BY date
        """)

        # Популярные категории
        top_categories = execute_query("""
            SELECT 
                COALESCE(c.name, 'Без категории') as category,
                COUNT(oi.id) as items_sold,
                COALESCE(SUM(oi.quantity * oi.price), 0) as revenue
            FROM firstapp_var_22_orderitem oi
            JOIN firstapp_var_22_book b ON oi.book_id = b.id
            LEFT JOIN firstapp_var_22_category c ON b.category_id = c.id
            JOIN firstapp_var_22_order o ON oi.order_id = o.id
            WHERE o.status = 'completed'
            GROUP BY c.name
            ORDER BY revenue DESC
            LIMIT 5
        """)

        return render_template('dashboard.html',
                               stats=stats,
                               today_stats=today_stats,
                               today_date=datetime.now().strftime('%d.%m.%Y'),
                               weekly_sales=weekly_sales,
                               top_categories=top_categories)

    except Exception as e:
        print(f"Ошибка в дашборде: {e}")
        flash(f"Ошибка загрузки дашборда: {e}", "danger")
        return render_template('dashboard.html', stats={})


@app.route('/books')
def books():
    """Страница книг"""
    try:
        # Параметры фильтрации
        search = request.args.get('search', '')
        category = request.args.get('category', 'all')
        min_price = request.args.get('min_price', '')
        max_price = request.args.get('max_price', '')
        page = request.args.get('page', 1, type=int)
        per_page = 20

        # Базовый запрос
        query = """
            SELECT 
                b.*,
                COALESCE(c.name, 'Без категории') as category_name
            FROM firstapp_var_22_book b
            LEFT JOIN firstapp_var_22_category c ON b.category_id = c.id
            WHERE 1=1
        """

        params = []

        if search:
            query += " AND (b.title ILIKE %s OR b.authors ILIKE %s)"
            params.extend([f'%{search}%', f'%{search}%'])

        if category != 'all':
            query += " AND c.name = %s"
            params.append(category)

        if min_price:
            query += " AND b.price >= %s"
            params.append(float(min_price))

        if max_price:
            query += " AND b.price <= %s"
            params.append(float(max_price))

        query += " ORDER BY b.title"

        # Получаем все книги
        all_books = execute_query(query, params)
        total_books = len(all_books)

        # Пагинация
        books = get_paginated_data(all_books, page, per_page)
        total_pages = (total_books + per_page - 1) // per_page

        # Категории для фильтра
        categories = execute_query("""
            SELECT DISTINCT name 
            FROM firstapp_var_22_category 
            WHERE name IS NOT NULL 
            ORDER BY name
        """)
        categories = [cat['name'] for cat in categories]

        return render_template('books.html',
                               books=books,
                               categories=categories,
                               search=search,
                               category=category,
                               min_price=min_price,
                               max_price=max_price,
                               page=page,
                               total_pages=total_pages,
                               total_books=total_books)

    except Exception as e:
        print(f"Ошибка при загрузке книг: {e}")
        flash(f"Ошибка загрузки книг: {e}", "danger")
        return render_template('books.html', books=[], categories=[])


@app.route('/orders')
def orders():
    """Страница заказов"""
    try:
        # Параметры фильтрации
        status = request.args.get('status', 'all')
        date_from = request.args.get('date_from', '')
        date_to = request.args.get('date_to', '')
        page = request.args.get('page', 1, type=int)
        per_page = 20

        # Базовый запрос
        query = """
            SELECT 
                o.*,
                u.username,
                u.email,
                (SELECT COUNT(*) FROM firstapp_var_22_orderitem WHERE order_id = o.id) as items_count
            FROM firstapp_var_22_order o
            LEFT JOIN firstapp_var_22_user u ON o.user_id = u.id
            WHERE 1=1
        """

        params = []

        if status != 'all':
            query += " AND o.status = %s"
            params.append(status)

        if date_from:
            query += " AND o.created >= %s"
            params.append(date_from)

        if date_to:
            query += " AND o.created <= %s"
            params.append(date_to + ' 23:59:59')

        query += " ORDER BY o.created DESC"

        # Получаем все заказы
        all_orders = execute_query(query, params)
        total_orders = len(all_orders)

        # Пагинация
        orders = get_paginated_data(all_orders, page, per_page)
        total_pages = (total_orders + per_page - 1) // per_page

        return render_template('orders.html',
                               orders=orders,
                               status=status,
                               date_from=date_from,
                               date_to=date_to,
                               page=page,
                               total_pages=total_pages,
                               total_orders=total_orders)

    except Exception as e:
        print(f"Ошибка при загрузке заказов: {e}")
        flash(f"Ошибка загрузки заказов: {e}", "danger")
        return render_template('orders.html', orders=[])


@app.route('/customers')
def customers():
    """Страница клиентов"""
    try:
        # Параметры поиска
        search = request.args.get('search', '')
        page = request.args.get('page', 1, type=int)
        per_page = 20

        # Базовый запрос
        query = "SELECT * FROM firstapp_var_22_user WHERE 1=1"
        params = []

        if search:
            query += " AND (username ILIKE %s OR email ILIKE %s)"
            params.extend([f'%{search}%', f'%{search}%'])

        query += " ORDER BY date_joined DESC"

        # Получаем всех клиентов
        all_customers = execute_query(query, params)
        total_customers = len(all_customers)

        # Добавляем статистику по заказам для каждого клиента
        for customer in all_customers:
            order_stats = execute_query("""
                SELECT 
                    COUNT(*) as order_count,
                    COALESCE(SUM(total), 0) as total_spent
                FROM firstapp_var_22_order
                WHERE user_id = %s AND status = 'completed'
            """, [customer['id']])

            if order_stats:
                customer['order_count'] = order_stats[0]['order_count'] or 0
                customer['total_spent'] = float(order_stats[0]['total_spent'] or 0)
            else:
                customer['order_count'] = 0
                customer['total_spent'] = 0.0

        # Пагинация
        customers = get_paginated_data(all_customers, page, per_page)
        total_pages = (total_customers + per_page - 1) // per_page

        return render_template('customers.html',
                               customers=customers,
                               search=search,
                               page=page,
                               total_pages=total_pages,
                               total_customers=total_customers)

    except Exception as e:
        print(f"Ошибка при загрузке клиентов: {e}")
        flash(f"Ошибка загрузки клиентов: {e}", "danger")
        return render_template('customers.html', customers=[])


@app.route('/analytics')
def analytics():
    """Страница аналитики"""
    return render_template('analytics.html')


@app.route('/search')
def search():
    """Страница поиска"""
    query = request.args.get('q', '')

    if not query:
        flash('Введите поисковый запрос', 'info')
        return redirect(url_for('index'))

    try:
        search_term = f'%{query}%'

        # Ищем книги
        books = execute_query("""
            SELECT 'book' as type, id, title as name, authors as description, created
            FROM firstapp_var_22_book
            WHERE title ILIKE %s OR authors ILIKE %s OR isbn ILIKE %s
            LIMIT 10
        """, [search_term, search_term, search_term])

        # Ищем заказы
        orders = execute_query("""
            SELECT 'order' as type, o.id, CONCAT('Заказ #', o.id) as name, 
                   u.username as description, o.created
            FROM firstapp_var_22_order o
            LEFT JOIN firstapp_var_22_user u ON o.user_id = u.id
            WHERE CAST(o.id AS TEXT) ILIKE %s OR u.username ILIKE %s
            LIMIT 10
        """, [search_term, search_term])

        # Ищем клиентов
        customers = execute_query("""
            SELECT 'customer' as type, id, username as name, email as description, date_joined as created
            FROM firstapp_var_22_user
            WHERE username ILIKE %s OR email ILIKE %s
            LIMIT 10
        """, [search_term, search_term])

        # Объединяем результаты
        results = list(books) + list(orders) + list(customers)

        return render_template('search.html',
                               query=query,
                               results=results,
                               books_count=len(books),
                               orders_count=len(orders),
                               customers_count=len(customers))

    except Exception as e:
        print(f"Ошибка поиска: {e}")
        flash(f'Ошибка при поиске: {str(e)}', 'danger')
        return render_template('search.html', query=query, results=[])


@app.route('/export/books/csv')
def export_books_csv():
    """Экспорт книг в CSV"""
    try:
        books = execute_query("""
            SELECT 
                title, authors, isbn, price, stock, available,
                publication_year, created
            FROM firstapp_var_22_book
            ORDER BY title
        """)

        if not books:
            flash('Нет данных для экспорта', 'warning')
            return redirect(url_for('books'))

        # Создаем CSV файл
        filepath = get_export_path('books_export')

        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=books[0].keys())
            writer.writeheader()
            writer.writerows(books)

        return send_file(filepath, as_attachment=True)

    except Exception as e:
        flash(f'Ошибка при экспорте: {str(e)}', 'danger')
        return redirect(url_for('books'))


@app.route('/export/orders/csv')
def export_orders_csv():
    """Экспорт заказов в CSV"""
    try:
        orders = execute_query("""
            SELECT 
                o.id, o.created, o.status, o.total, o.payment_method,
                u.username, u.email,
                (SELECT COUNT(*) FROM firstapp_var_22_orderitem WHERE order_id = o.id) as items_count
            FROM firstapp_var_22_order o
            LEFT JOIN firstapp_var_22_user u ON o.user_id = u.id
            ORDER BY o.created DESC
        """)

        if not orders:
            flash('Нет данных для экспорта', 'warning')
            return redirect(url_for('orders'))

        # Создаем CSV файл
        filepath = get_export_path('orders_export')

        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=orders[0].keys())
            writer.writeheader()
            writer.writerows(orders)

        return send_file(filepath, as_attachment=True)

    except Exception as e:
        flash(f'Ошибка при экспорте: {str(e)}', 'danger')
        return redirect(url_for('orders'))


# ==================== API ====================

@app.route('/api/status')
def api_status():
    """API: Проверка статуса системы"""
    try:
        # Проверяем подключение к базе
        success, message = check_database_connection()

        # Базовая статистика
        stats = execute_query("""
            SELECT 
                (SELECT COUNT(*) FROM firstapp_var_22_book) as books,
                (SELECT COUNT(*) FROM firstapp_var_22_order) as orders,
                (SELECT COUNT(*) FROM firstapp_var_22_user) as users
        """)[0]

        return jsonify({
            'success': success,
            'message': message,
            'status': 'running',
            'timestamp': datetime.now().isoformat(),
            'database': {
                'books': stats['books'],
                'orders': stats['orders'],
                'users': stats['users']
            }
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e),
            'status': 'error'
        }), 500


# ==================== ЗАПУСК ====================

if __name__ == '__main__':
    print("=" * 60)
    print("📊 Аналитическая панель книжного магазина")
    print("=" * 60)

    # Проверка подключения к базе
    success, message = check_database_connection()
    print(message)

    if not success:
        print("⚠️  Приложение запущено с ошибками подключения")
        print("Проверьте настройки в config.py")

    # Только одна ссылка - localhost
    print(f"🚀 Сервер запущен: http://127.0.0.1:5001")
    print("=" * 60)

    # Запускаем только на localhost (127.0.0.1), а не на всех интерфейсах (0.0.0.0)
    app.run(debug=True, host='127.0.0.1', port=5001)