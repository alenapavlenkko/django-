from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('navigator/', views.navigator, name='navigator'),
    path('books/', views.book_list, name='book_list'),
    path('books/page/<int:page>/', views.book_list, name='book_list_page'),
    path('books/page/', views.book_list, {'page': 1}, name='book_list_page_default'),
    path('book/<slug:slug>/', views.book_detail, name='book_detail'),
    path('book/<slug:slug>/<int:year>/', views.book_detail, name='book_detail_year'),
    path('purchase/success/<int:pk>/', views.purchase_success, name='purchase_success'),
    path('buy/', views.buy_book, name='buy_book'),
    path('buy/<int:book_id>/', views.buy_book, name='buy_book_item'),
    path('thank_you/', views.thank_you, name='thank_you'),
    path('analysis/', views.order_analysis, name='order_analysis'),
    path('products-demo/', views.products_demo, name='products_demo'),
    path('simple-data/', views.simple_data, name='simple_data'),
    path('export/', views.export_orders, name='export_orders'),

    # Таблицы
    path('tablica/', views.tablica_display, name='tablica_display'),
    path('tablica/text/', views.tablica_from_text, name='tablica_text'),
    path('tablica/xlsx/', views.tablica_from_xlsx, name='tablica_xlsx'),

    # Редирект старого адреса
    path('old-books/', views.redirect_old_books, name='old_books'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
