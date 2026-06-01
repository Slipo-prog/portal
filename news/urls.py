from django.urls import path
from . import views  # импортируем наши представления из views.py

urlpatterns = [
    # path(адрес, функция, имя_маршрута)

    # Когда пользователь заходит на /news/ — вызываем news_list
    path('', views.news_list, name='news_list'),

    # Когда пользователь заходит на /news/123/ — вызываем news_detail
    # <int:news_id> — это "динамический сегмент". Django достанет число из адреса
    # и передаст его в функцию как параметр news_id
    path('<int:news_id>/', views.news_detail, name='news_detail'),
]