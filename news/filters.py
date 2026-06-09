import django_filters
from django import forms
from .models import Post, Author
from django.contrib.auth.models import User


class PostFilter(django_filters.FilterSet):
    # Фильтр по названию (содержит)
    title = django_filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Название содержит'
    )

    # Фильтр по имени автора (через связанную модель User)
    author__user__username = django_filters.CharFilter(
        field_name='author__user__username',
        lookup_expr='icontains',
        label='Имя автора'
    )

    # Фильтр по дате (позже указанной)
    created_at = django_filters.DateFilter(
        field_name='created_at',
        lookup_expr='gte',
        label='Новости позже даты',
        widget=forms.DateInput(attrs={'type': 'date'})  # календарь
    )

    class Meta:
        model = Post
        fields = ['title', 'author__user__username', 'created_at']