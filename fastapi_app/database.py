"""
Простое подключение к PostgreSQL
"""
import psycopg2
from psycopg2.extras import RealDictCursor

# Настройки из вашего Django
DB_CONFIG = {
    "host": "localhost",
    "port": "5432",
    "database": "bookshop_fresh",
    "user": "bookshop_user",
    "password": "secure_password_123"
}


def get_connection():
    """Получить соединение с БД"""
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


def get_books():
    """Получить список книг"""
    conn = get_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor()
        # Пробуем получить книги с авторами
        query = """
            SELECT b.id, b.title, b.price, b.description,
                   a.first_name || ' ' || a.last_name as author
            FROM firstapp_var_22_book b
            LEFT JOIN firstapp_var_22_author a ON b.author_id = a.id
            ORDER BY b.id
            LIMIT 50
        """
        cursor.execute(query)
        books = cursor.fetchall()
        return books
    except:
        # Если сложный запрос не работает, делаем простой
        try:
            cursor.execute("SELECT * FROM firstapp_var_22_book LIMIT 20")
            return cursor.fetchall()
        except:
            return []
    finally:
        conn.close()


def get_stats():
    """Получить базовую статистику"""
    conn = get_connection()
    if not conn:
        return {"books": 0, "users": 0}

    try:
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) as count FROM firstapp_var_22_book")
        books_count = cursor.fetchone()["count"]

        cursor.execute("SELECT COUNT(*) as count FROM firstapp_var_22_user")
        users_count = cursor.fetchone()["count"]

        return {"books": books_count, "users": users_count}
    except:
        return {"books": 0, "users": 0}
    finally:
        conn.close()