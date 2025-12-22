"""
Модуль для работы с базой данных
"""

import psycopg2
from psycopg2.extras import RealDictCursor
from config import DB_CONFIG


def get_db_connection():
    """
    Установка соединения с PostgreSQL базой данных Django

    Returns:
        psycopg2.connection: Соединение с базой данных
    """
    try:
        conn = psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)
        return conn
    except Exception as e:
        print(f"Ошибка подключения к базе данных: {e}")
        raise


def execute_query(query, params=None):
    """
    Выполнение SQL запроса и возврат результатов

    Args:
        query (str): SQL запрос
        params (tuple, optional): Параметры запроса

    Returns:
        list: Результаты запроса
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        if params:
            cur.execute(query, params)
        else:
            cur.execute(query)

        results = cur.fetchall()

        cur.close()
        conn.close()

        return results

    except Exception as e:
        print(f"Ошибка выполнения запроса: {e}")
        return []


def get_table_count(table_name):
    """
    Получить количество записей в таблице

    Args:
        table_name (str): Имя таблицы

    Returns:
        int: Количество записей
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        query = f"SELECT COUNT(*) as count FROM {table_name}"
        cur.execute(query)
        result = cur.fetchone()

        cur.close()
        conn.close()

        return result['count']
    except Exception as e:
        print(f"Ошибка получения количества записей: {e}")
        return 0


def check_database_connection():
    """
    Проверка подключения к базе данных

    Returns:
        tuple: (успешно, сообщение)
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Проверяем версию PostgreSQL
        cur.execute("SELECT version();")
        version = cur.fetchone()['version']

        # Проверяем основные таблицы
        tables_to_check = [
            'firstapp_var_22_book',
            'firstapp_var_22_order',
            'firstapp_var_22_user'
        ]

        existing_tables = []
        for table in tables_to_check:
            try:
                cur.execute(f"SELECT 1 FROM {table} LIMIT 1")
                existing_tables.append(table)
            except:
                pass

        cur.close()
        conn.close()

        return True, f"✅ Подключено к PostgreSQL {version}. Найдено таблиц: {len(existing_tables)}"

    except Exception as e:
        return False, f"❌ Ошибка подключения: {e}"