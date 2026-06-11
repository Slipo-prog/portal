from celery import shared_task
from .utils import send_weekly_newsletter
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Post


@shared_task
def weekly_newsletter_task():
    """Задача для еженедельной рассылки"""
    send_weekly_newsletter()


@shared_task
def notify_subscribers_about_new_post(post_id):
    """Асинхронная задача: уведомить подписчиков о новой статье"""
    try:
        post = Post.objects.get(id=post_id)

        # Получаем всех подписчиков категорий этой статьи
        categories = post.categories.all()
        subscribers = set()

        for category in categories:
            for subscriber in category.subscribers.all():
                subscribers.add(subscriber)

        if not subscribers:
            return f'Нет подписчиков для статьи {post.title}'

        # Отправляем письма
        html_content = render_to_string('news/email/new_post_notification.html', {
            'post': post,
            'post_url': post.get_absolute_url(),
        })

        text_content = f'Новая статья: {post.title}\nЧитать: http://127.0.0.1:8000{post.get_absolute_url()}'

        for subscriber in subscribers:
            msg = EmailMultiAlternatives(
                subject=f'Новая статья! {post.title}',
                body=text_content,
                from_email=None,
                to=[subscriber.email],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()

        return f'Уведомления отправлены {len(subscribers)} подписчикам для статьи {post.title}'

    except Post.DoesNotExist:
        return f'Статья с id={post_id} не найдена'