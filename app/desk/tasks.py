from celery import shared_task
from django.core.mail import EmailMessage

from desk.models import Desk


@shared_task
def send_mail(desk_id):
    desk = Desk.objects.get(id=desk_id)
    email = EmailMessage(
        'HelpDesk',
        f'Your application: {desk.title} has been completed',
        to=[str(desk.User.email)]
    )
    email.send()
