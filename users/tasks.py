import uuid
from datetime import timedelta

from celery import shared_task
from django.utils.timezone import now

from users.models import EmailVerification, User


@shared_task
def send_email_verification(user_id: int):
    record = EmailVerification.objects.create(
        code=uuid.uuid4(),
        user=User.objects.get(id=user_id),
        expiration=now() + timedelta(hours=48)
    )
    record.send_verification_email()
