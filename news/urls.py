from django.urls import path
from . import views  # импортируем наши представления из views.py

from django.urls import path
from . import views

urlpatterns = [
    # Список новостей (используем класс NewsListView)
    path('', views.NewsListView.as_view(), name='news_list'),

    # Поиск
    path('search/', views.SearchView.as_view(), name='search'),

    # Детальный просмотр
    path('<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),

    # Создание
    path('create/', views.NewsCreateView.as_view(), name='news_create'),
    path('articles/create/', views.ArticleCreateView.as_view(), name='article_create'),

    # Редактирование
    path('<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_edit'),
    path('articles/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_edit'),

    # Удаление
    path('<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('articles/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),


    path('become_author/', views.become_author, name='become_author'),


    path('subscribe/', views.subscribe_to_category, name='subscribe_to_category'),
    path('unsubscribe/<int:category_id>/', views.unsubscribe_from_category, name='unsubscribe'),
]