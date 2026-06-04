from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from .models import Post
from .forms import PostForm



# Список новостей с пагинацией
class NewsListView(ListView):
    model = Post
    template_name = 'news/news_list.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(post_type='NE').order_by('-created_at')


# Поиск (если ещё нет)
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


# Создание новости
class NewsCreateView(BasePostCreateView):
    post_type = 'NE'


# Создание статьи
class ArticleCreateView(BasePostCreateView):
    post_type = 'AR'


# Редактирование (общее)
class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'news/post_form.html'

    def get_success_url(self):
        return reverse_lazy('post_detail', args=[self.object.pk])


# Удаление
class PostDeleteView(DeleteView):
    model = Post
    template_name = 'news/post_confirm_delete.html'
    success_url = reverse_lazy('news_list')


# Детальный просмотр
class PostDetailView(DetailView):
    model = Post
    template_name = 'news/post_detail.html'
    context_object_name = 'post'