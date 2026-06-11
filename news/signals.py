from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from django.dispatch import receiver
from .models import Post
from .tasks import notify_subscribers_about_new_post  # ← ИМПОРТ ИЗ TASKS (а не из utils)
from .utils import send_welcome_email


@receiver(post_save, sender=User)
def add_user_to_common_group(sender, instance, created, **kwargs):
    """Автоматически добавляем нового пользователя в группу 'common' и отправляем приветственное письмо"""
    if created:
        try:
            common_group = Group.objects.get(name='common')
            instance.groups.add(common_group)
        except Group.DoesNotExist:
            # Если группы 'common' не существует, создаём её
            common_group = Group.objects.create(name='common')
            instance.groups.add(common_group)

        # Отправляем приветственное письмо новому пользователю
        send_welcome_email(instance)


@receiver(post_save, sender=Post)
def notify_subscribers_on_new_post(sender, instance, created, **kwargs):
    """Асинхронно уведомляем подписчиков о новой статье через Celery"""
    if created:
        # Запускаем асинхронную задачу вместо прямого вызова
        notify_subscribers_about_new_post.delay(instance.id)
        print(f'🚀 Асинхронная задача на уведомление запущена для статьи {instance.title}')