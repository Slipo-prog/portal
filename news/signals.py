from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from django.dispatch import receiver


@receiver(post_save, sender=User)
def add_user_to_common_group(sender, instance, created, **kwargs):
    """Автоматически добавляем нового пользователя в группу 'common'"""
    if created:
        try:
            common_group = Group.objects.get(name='common')
            instance.groups.add(common_group)
        except Group.DoesNotExist:
            # Если группы 'common' не существует, создаём её
            common_group = Group.objects.create(name='common')
            instance.groups.add(common_group)