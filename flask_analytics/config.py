"""
Конфигурация приложения
"""

import os
from datetime import datetime

# Конфигурация базы данных PostgreSQL (Django)
DB_CONFIG = {
    'dbname': 'bookshop_fresh',
    'user': 'bookshop_user',
    'password': 'secure_password_123',  # Замените на ваш пароль
    'host': 'localhost',
    'port': '5432'
}

# Настройки приложения
SECRET_KEY = 'bookshop-analytics-secret-key-2024'
EXPORTS_DIR = 'exports'
ITEMS_PER_PAGE = 20

# Пути для экспорта
def get_export_path(filename):
    """Получить путь для файла экспорта"""
    os.makedirs(EXPORTS_DIR, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return os.path.join(EXPORTS_DIR, f'{filename}_{timestamp}.csv')