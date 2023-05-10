from django.conf import settings
from django.core import mail

from projeto.celery import app


@app.task
def email_admins_teste():
    mail.send_mail('tarefa teste', 'Tarefa teste enviada via celery worker',
                   from_email=settings.DEFAULT_FROM_EMAIL,
                   recipient_list=dict(settings.ADMINS).values())
