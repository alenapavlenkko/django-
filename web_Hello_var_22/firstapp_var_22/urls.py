# firstapp_var_22/urls.py
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('navigator/', views.navigator, name='navigator'),

    # Книги
    path('books/', views.book_list, name='book_list'),
    path('books/page/<int:page>/', views.book_list, name='book_list_page'),
    path('book/<slug:slug>/', views.book_detail, name='book_detail'),
    path('book/<slug:slug>/<int:year>/', views.book_detail, name='book_detail_year'),
    path('fastapi/', views.fastapi_redirect, name='fastapi-redirect'),

    # Заказы
    path('buy/', views.buy_book, name='buy_book'),
    path('buy/<int:book_id>/', views.buy_book, name='buy_book_item'),
    path('order/success/<int:pk>/', views.order_success, name='order_success'),
    path('orders/history/', views.order_history, name='order_history'),
    path('orders/analysis/', views.order_analysis, name='order_analysis'),

    # Статические страницы
    path('thank_you/', views.thank_you, name='thank_you'),
    path('products-demo/', views.products_demo, name='products_demo'),  # БЫЛО: 'products_demo'
    path('reviews/', views.reviews, name='reviews'),
    path('analysis/', views.analysis, name='analysis'),
    path('export/', views.export_orders, name='export_orders'),

    # Таблицы
    path('tablica/csv/', views.tablica_display, name='tablica_csv'),
    path('tablica/txt/', views.tablica_from_text, name='tablica_txt'),
    path('tablica/xlsx/', views.tablica_from_xlsx, name='tablica_xlsx'),

    # Редиректы
    path('old-books/', views.redirect_old_books, name='old_books'),

    # Файлы книг
    path('files/books/', views.files_books, name='files_books'),
]

# Для медиа файлов в development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)