from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils.timezone import now


class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', null=True, blank=True)
    is_verified_email = models.BooleanField(default=False)
    email = models.EmailField(unique=True)

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'


class EmailVerification(models.Model):
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    def _generate_email_verification_link(self) -> str:
        link = reverse('users:email_verification', kwargs={'email': self.user.email, 'code': self.code})
        return f'{settings.DOMAIN_NAME}{link}'

    def send_verification_email(self) -> None:
        subject = f'Подтверждение учетной записи для {self.user.username}'
        message = 'Для подтверждения учетной записи перейдите по ссылке:'
        send_mail(
            subject=subject,
            message=message + '\n' + self._generate_email_verification_link(),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user.email],
            fail_silently=False,
        )

    def is_expired(self) -> bool:
        return True if now() >= self.expiration else False

    def __str__(self) -> str:
        return f'Email verification object for {self.user.email}'
