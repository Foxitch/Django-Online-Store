from django.test import TestCase
from django.urls import reverse

from users.models import User


class UserRegistrationViewTest(TestCase):

    def setUp(self) -> None:
        self.path = reverse('users:registration')

    def test_user_registration_view_status_code(self):
        response = self.client.get(path=self.path)

        self.assertEqual(
            first=response.status_code,
            second=200,
            msg=f'Expected status code is 200, actual is {response.status_code}'
        )

    def test_user_registration_view_title(self):
        response = self.client.get(self.path)

        self.assertEqual(
            first=response.context_data['title'],
            second='Store - Регистрация',
            msg=f'Expected title is "Store - Регистрация", actual is "{response.context_data["title"]}"'
        )

    def test_user_registration_view_template_used(self):
        response = self.client.get(path=self.path)

        self.assertTemplateUsed(
            response=response,
            template_name='users/registration.html',
            msg_prefix='Unexpected template is used'
        )

    def test_user_registration_success(self):
        data = {
            'first_name': 'test',
            'last_name': 'user',
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        response = self.client.post(path=reverse('users:registration'), data=data)
        self.assertEqual(
            first=response.status_code,
            second=302,
            msg=f'Expected status code is 302, actual is {response.status_code}'
        )
        self.assertTrue(
            expr=User.objects.filter(username='testuser').exists(),
            msg='Created user was not found in the DB'
        )

    def test_user_registration_password_mismatch(self):
        data = {
            'first_name': 'test',
            'last_name': 'user',
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword1234',
        }
        response = self.client.post(path=reverse('users:registration'), data=data)
        self.assertEqual(
            first=response.status_code,
            second=200,
            msg=f'Expected status code is 200, actual is {response.status_code}'
        )
        self.assertContains(
            response=response,
            text='Введенные пароли не совпадают.',
            msg_prefix='Response does not contain expected text'
        )
