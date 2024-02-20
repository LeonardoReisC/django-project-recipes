from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AuthorsLogoutTest(TestCase):

    def test_logout_shows_error_message_if_not_POST_method(self):
        User.objects.create_user(username='my_user', password='my_pass')
        self.client.login(username='my_user', password='my_pass')

        response = self.client.get(reverse('authors:logout'), follow=True)

        self.assertIn(
            'Invalid logout request.',
            response.content.decode('utf-8')
        )

    def test_logout_shows_error_message_if_not_logged_user(self):
        User.objects.create_user(username='my_user', password='my_pass')
        self.client.login(username='my_user', password='my_pass')

        response = self.client.post(
            reverse('authors:logout'),
            data={
                'username': 'another_user'
            },
            follow=True)

        self.assertIn(
            'Invalid logout user.',
            response.content.decode('utf-8')
        )

    def test_user_can_logout_successfully(self):
        User.objects.create_user(username='my_user', password='my_pass')
        self.client.login(username='my_user', password='my_pass')

        response = self.client.post(
            reverse('authors:logout'),
            data={
                'username': 'my_user'
            },
            follow=True)

        self.assertIn(
            'Logged out successfully.',
            response.content.decode('utf-8')
        )
