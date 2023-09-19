from typing import Any

from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from common.views import TitleMixin
from users.forms import UserLoginForm, UserProfileForm, UserRegistrationForm
from users.models import EmailVerification, User


class UserLoginView(TitleMixin, LoginView):
    form_class = UserLoginForm
    title = 'Store - Авторизация'
    template_name = 'users/login.html'


class UserRegistrationView(TitleMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    title = 'Store - Регистрация'
    success_url = reverse_lazy('users:login')
    success_message = 'Вы успешно зарегистрированы! Подтвердите ваш Email'
    template_name = 'users/registration.html'


class UserProfileView(TitleMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    title = 'Store - Личный кабинет'
    template_name = 'users/profile.html'

    def get_success_url(self) -> Any:
        return reverse_lazy('users:profile', args=(self.object.id,))


class EmailVerificationView(TitleMixin, TemplateView):
    template_name = 'users/email_verification.html'
    title = 'Store - Подтверждение регистрации'

    def is_email_verified(self, user: str, code: str) -> bool:
        email_verification = EmailVerification.objects.filter(user=user, code=code)
        return all([
            email_verification.exists(),
            not email_verification.first().is_expired()
        ])

    def get(self, request, *args, **kwargs) -> TemplateResponse | HttpResponseRedirect:
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])

        if self.is_email_verified(user=user, code=code):
            user.is_verified_email = True
            user.save()
            return super().get(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('index'))
