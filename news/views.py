from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin  
from .models import Post
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib import messages


# Список новостей с пагинацией
class NewsListView(ListView):
    model = Post
    template_name = 'news/news_list.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(post_type='NE').order_by('-created_at')


# Поиск
from django_filters.views import FilterView
from .filters import PostFilter


class SearchView(FilterView):
    model = Post
    template_name = 'news/search.html'
    context_object_name = 'posts'
    filterset_class = PostFilter
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.all().order_by('-created_at')


# Базовый класс для создания (устанавливает post_type)
class BasePostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'news/post_form.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = self.post_type
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_detail', args=[self.object.pk])


# Создание новости (с проверкой аутентификации)
class NewsCreateView(LoginRequiredMixin, BasePostCreateView):  # ← ДОБАВИТЬ LoginRequiredMixin
    post_type = 'NE'


# Создание статьи (с проверкой аутентификации)
class ArticleCreateView(LoginRequiredMixin, BasePostCreateView):  # ← ДОБАВИТЬ LoginRequiredMixin
    post_type = 'AR'


# Редактирование (с проверкой аутентификации)
class PostUpdateView(LoginRequiredMixin, UpdateView):  # ← ДОБАВИТЬ LoginRequiredMixin
    model = Post
    form_class = PostForm
    template_name = 'news/post_form.html'

    def get_success_url(self):
        return reverse_lazy('post_detail', args=[self.object.pk])


# Удаление (с проверкой аутентификации)
class PostDeleteView(LoginRequiredMixin, DeleteView):  # ← ДОБАВИТЬ LoginRequiredMixin
    model = Post
    template_name = 'news/post_confirm_delete.html'
    success_url = reverse_lazy('news_list')


# Детальный просмотр (без проверки - доступен всем)
class PostDetailView(DetailView):
    model = Post
    template_name = 'news/post_detail.html'
    context_object_name = 'post'


@login_required
def become_author(request):
    """Добавляет пользователя в группу authors"""
    author_group = Group.objects.get(name='authors')

    if request.user not in author_group.user_set.all():
        author_group.user_set.add(request.user)
        messages.success(request, 'Поздравляем! Вы стали автором!')
    else:
        messages.info(request, 'Вы уже являетесь автором.')

    return redirect('news_list')