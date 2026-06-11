from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from .models import Category, Post
from datetime import datetime, timedelta
from django.utils import timezone


def send_new_post_notification(post):
    """Отправка уведомления подписчикам категории о новой статье"""
    categories = post.categories.all()
    subscribers = set()

    for category in categories:
        for subscriber in category.subscribers.all():
            subscribers.add(subscriber)

    if not subscribers:
        return

    html_content = render_to_string('news/email/new_post_notification.html', {
        'post': post,
        'post_url': post.get_absolute_url(),
    })

    text_content = f'Новая статья: {post.title}\nЧитать: {post.get_absolute_url()}'

    for subscriber in subscribers:
        try:
            msg = EmailMultiAlternatives(
                subject=f'Новая статья в категории! {post.title}',
                body=text_content,
                from_email=None,  # используется DEFAULT_FROM_EMAIL
                to=[subscriber.email],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
        except Exception as e:
            print(f'Ошибка отправки письма для {subscriber.email}: {e}')


def send_weekly_newsletter():
    """Еженедельная рассылка новых статей за неделю"""
    week_ago = timezone.now() - timedelta(days=7)
    new_posts = Post.objects.filter(created_at__gte=week_ago).order_by('-created_at')

    if not new_posts:
        return

    # Группируем статьи по категориям
    categories = Category.objects.all()

    for category in categories:
        category_posts = new_posts.filter(categories=category)
        if not category_posts:
            continue

        subscribers = category.subscribers.all()
        if not subscribers:
            continue

        for subscriber in subscribers:
            html_content = render_to_string('news/email/weekly_newsletter.html', {
                'user': subscriber,
                'category': category,
                'posts': category_posts,
                'week_start': week_ago,
            })

            text_content = f'Новые статьи в категории "{category.name}" за неделю: {", ".join([p.title for p in category_posts])}'

            try:
                msg = EmailMultiAlternatives(
                    subject=f'Еженедельная рассылка: новые статьи в категории "{category.name}"',
                    body=text_content,
                    from_email=None,
                    to=[subscriber.email],
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()
            except Exception as e:
                print(f'Ошибка отправки рассылки для {subscriber.email}: {e}')


def send_welcome_email(user):
    """Приветственное письмо при регистрации"""
    html_content = render_to_string('news/email/welcome_email.html', {
        'user': user,
    })

    text_content = f'Приветствуем вас, {user.username or user.email}! Рады видеть вас в нашем Новостном портале.'

    try:
        msg = EmailMultiAlternatives(
            subject='Добро пожаловать в Новостной портал!',
            body=text_content,
            from_email=None,
            to=[user.email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    except Exception as e:
        print(f'Ошибка отправки приветственного письма для {user.email}: {e}')