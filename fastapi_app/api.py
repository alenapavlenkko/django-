"""
FastAPI приложение с HTML шаблонами - упрощенная версия
"""
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import psycopg2
from psycopg2.extras import RealDictCursor
from pathlib import Path
from decimal import Decimal
from datetime import datetime, date

# Создаем приложение
app = FastAPI(
    title="Книжный магазин",
    version="1.0"
)

# Настройки подключения
DB_CONFIG = {
    "host": "localhost",
    "port": "5432",
    "database": "bookshop_fresh",
    "user": "bookshop_user",
    "password": "secure_password_123"
}

# Настраиваем шаблоны
templates_dir = Path(__file__).parent / "templates"
templates = Jinja2Templates(directory=str(templates_dir))

def get_db():
    """Подключение к базе данных"""
    try:
        conn = psycopg2.connect(
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            database=DB_CONFIG["database"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            cursor_factory=RealDictCursor
        )
        return conn
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        return None

def convert_for_json(data):
    """Рекурсивно преобразовывает типы данных для JSON"""
    if isinstance(data, dict):
        return {k: convert_for_json(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_for_json(item) for item in data]
    elif isinstance(data, Decimal):
        return float(data)
    elif isinstance(data, (datetime, date)):
        return data.isoformat()
    else:
        return data

def get_books():
    """Получить книги из таблицы firstapp_var_22_book"""
    conn = get_db()
    if not conn:
        return []

    try:
        cursor = conn.cursor()
        query = "SELECT * FROM firstapp_var_22_book ORDER BY id LIMIT 50"
        cursor.execute(query)
        books = cursor.fetchall()

        # Преобразуем в список словарей
        books_list = []
        for book in books:
            book_dict = {}
            for key in book.keys():
                book_dict[key] = book[key]
            books_list.append(book_dict)

        return books_list

    except Exception as e:
        print(f"❌ Ошибка получения книг: {e}")
        return []
    finally:
        conn.close()

# Главная страница
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    books_data = get_books()

    return templates.TemplateResponse("index.html", {
        "request": request,
        "book_count": len(books_data),
        "db_name": DB_CONFIG["database"],
        "db_connected": get_db() is not None
    })

# Страница с книгами
@app.get("/books", response_class=HTMLResponse)
async def books(request: Request):
    books_data = get_books()

    return templates.TemplateResponse("books.html", {
        "request": request,
        "books": books_data,
        "total_books": len(books_data),
        "table_name": "firstapp_var_22_book",
        "db_name": DB_CONFIG["database"]
    })

# API для получения книг в JSON
@app.get("/api/books")
async def api_books():
    books_data = get_books()
    books_converted = convert_for_json(books_data)

    return {
        "success": True,
        "count": len(books_converted),
        "books": books_converted
    }

if __name__ == "__main__":
    import uvicorn

    print("=" * 60)
    print("🚀 Запуск FastAPI приложения...")
    print(f"📊 База данных: {DB_CONFIG['database']}")
    print("🌐 Доступные страницы:")
    print("   http://localhost:8000/ - Главная страница")
    print("   http://localhost:8000/books - Список книг")
    print("   http://localhost:8000/docs - Документация API")
    print("=" * 60)

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)