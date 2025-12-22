# Система аналитики книжного магазина

## Описание проекта
Веб-приложение для управления и анализа данных книжного интернет-магазина.

## Структура базы данных
11 таблиц:
1. `firstapp_var_22_category` - Категории книг
2. `firstapp_var_22_author` - Авторы
3. `firstapp_var_22_publisher` - Издательства
4. `firstapp_var_22_book` - Книги
5. `firstapp_var_22_bookauthor` - Связь книги-авторы
6. `firstapp_var_22_bookdetail` - Детали книг
7. `firstapp_var_22_customer` - Клиенты
8. `firstapp_var_22_order` - Заказы
9. `firstapp_var_22_purchase` - Покупки
10. `firstapp_var_22_purchaseitem` - Позиции покупок
11. `firstapp_var_22_review` - Отзывы

## Установка и запуск

1. Клонировать репозиторий
2. Установить зависимости:
   ```bash
   pip install -r requirements.txt