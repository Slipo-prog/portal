from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from django.dispatch import receiver
from .models import Post
from .utils import send_new_post_notification, send_welcome_email  # нужно будет создать utils.py


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
    """Уведомляем подписчиков о новой статье"""
    if created:
        send_new_post_notification(instance)