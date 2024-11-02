from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Основні сторінки
    path('', views.quote_list, name='quote_list'),
    path('home/', views.home_view, name='home'),

    # Авторизація та профіль
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/profile/', views.profile_view, name='profile'),

    # Маршрути для цитат
    path('quotes/add/', views.add_quote, name='add_quote'),
    path('quotes/<int:id>/', views.quote_detail, name='quote_detail'),
    path('quotes/edit/<int:id>/', views.edit_quote, name='edit_quote'),
    path('quotes/delete/<int:id>/', views.delete_quote, name='delete_quote'),

    # Маршрути для авторів
    path('authors/', views.author_list, name='author_list'),
    path('authors/add/', views.add_author, name='add_author'),
    path('authors/<int:id>/', views.author_detail, name='author_detail'),
    path('authors/edit/<int:id>/', views.edit_author, name='edit_author'),
    path('authors/delete/<int:id>/', views.delete_author, name='delete_author'),
]
