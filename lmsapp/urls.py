from django.contrib import admin
from django.urls import path,include
from .views import homeView,addBookView,addBook
from django.conf.urls.static import static
from django.conf import settings
from . import views


urlpatterns = [
    path("",homeView, name='home'),
    path("Addbook/",addBookView),
    path("Addbook/add",addBook),
    path('borrow/', views.borrow_view, name='borrow'),
    path('process_borrow/', views.process_borrow, name='process_borrow'),
    path('available_books/', views.available_books, name='available_books'),
    path('borrowed_books/', views.borrowed_books, name='borrowed_books'),
    path('borrow_book/', views.borrow_book, name='borrow_book'),
    path('return_books/', views.return_books_view, name='return_books'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
