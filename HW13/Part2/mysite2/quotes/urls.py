from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Основна сторінка
    path('', views.home_view, name='home'),  # Переконайтеся, що ім'я співпадає з шаблоном
    path('quotes/', views.quote_list, name='quote_list'),  # Залишаємо цей маршрут як головний список цитат

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
    path('tags/<str:tag_name>/', views.quotes_by_tag, name='quotes_by_tag'),
    path('search/', views.search_quotes_by_tag, name='search_quotes_by_tag'),

    # Маршрути для авторів
    path('authors/', views.author_list, name='author_list'),
    path('authors/add/', views.add_author, name='add_author'),
    path('authors/<int:id>/', views.author_detail, name='author_detail'),
    path('authors/edit/<int:id>/', views.edit_author, name='edit_author'),
    path('authors/delete/<int:id>/', views.delete_author, name='delete_author'),
    path('search_author/', views.search_quotes_by_author, name='search_quotes_by_author'),

    # Скидання пароля
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
