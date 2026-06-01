
from django.shortcuts import render, get_object_or_404
from .models import Post  # импортируем модель Post из models.py


def news_list(request):
    """
    Представление для страницы со списком всех новостей.

    request — объект запроса (содержит информацию о пользователе, браузере и т.д.)
    """

    # Берём из базы данных все записи, у которых post_type = 'NE' (новость)
    # Сортируем по дате создания: сначала новые
    news_list = Post.objects.filter(post_type='NE').order_by('-created_at')

    # Рендерим шаблон:
    #   - первый аргумент: request
    #   - второй: путь к шаблону
    #   - третий: словарь с данными для шаблона
    return render(request, 'news/news_list.html', {'news_list': news_list})


def news_detail(request, news_id):
    """
    Представление для страницы конкретной новости.

    request — объект запроса
    news_id — число из URL (например, 5 для /news/5/)
    """

    # Пытаемся найти новость в базе по id и post_type='NE'
    # Если не нашли — автоматически возвращаем ошибку 404
    news = get_object_or_404(Post, id=news_id, post_type='NE')

    # Рендерим шаблон с найденной новостью
    return render(request, 'news/news_detail.html', {'news': news})
# Create your views here.
