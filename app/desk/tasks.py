from celery import shared_task
from django.core.mail import EmailMessage

from desk.models import Desk


@shared_task
def send_mail_for_user(desk_id):
    desk = Desk.objects.get(id=desk_id)
    email = EmailMessage(
        'HelpDesk',
        f'Your application: {desk.title} has been completed.',
        to=[str(desk.User.email)]
    )
    email.send()


@shared_task
def send_employee_mail(desk_id):
    # TODO: Вынести за таску !!!!!!!!
    # employees = Employee.objects.filter(is_employee=True).values_list('pk', flat=True)
    # employees_emails = [User.objects.get(id=x).email for x in employees]
    for mail in employees_emails:
        send_mail_for_employee.delay(desk_id, mail)


@shared_task
def send_mail_for_employee(desk_id, mail):
    desk = Desk.objects.get(id=desk_id)
    email = EmailMessage(
        'NEW TICKET HelpDesk',
        f'Ticket: {desk.title}',
        to=[str(mail)]
    )
    email.send()


