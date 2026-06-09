from celery import shared_task
from .utils import send_weekly_newsletter


@shared_task
def weekly_newsletter_task():
    """Задача для еженедельной рассылки"""
    send_weekly_newsletter()