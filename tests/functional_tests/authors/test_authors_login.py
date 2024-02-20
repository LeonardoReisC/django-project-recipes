from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By
import pytest

from .base import AuthorsBaseFunctionalTest


@pytest.mark.functional_tests
class AuthorsLoginFunctionalTest(AuthorsBaseFunctionalTest):
    def get_by_placeholder(self, form, placeholder):
        return form.find_element(
            By.XPATH,
            f'//input[@placeholder="{placeholder}"]'
        )

    def test_user_valid_data_can_login_successfully(self):
        string_password = 'pass'
        user = User.objects.create_user(
            username='my_user', password=string_password)

        # Open login page
        self.browser.get(self.live_server_url + reverse('authors:login'))

        # See login form
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        username_field = self.get_by_placeholder(
            form, 'Type your username here'
        )
        password_field = self.get_by_placeholder(
            form, 'Type your password here'
        )

        # Type username and password
        username_field.send_keys(user.username)
        password_field.send_keys(string_password)

        # Submit form
        form.submit()

        # See login success message
        self.assertIn(
            'as my_user',
            self.browser.find_element(By.TAG_NAME, 'main').text
        )

    def test_login_create_raises_404_if_not_POST_method(self):
        self.browser.get(
            self.live_server_url + reverse('authors:login_create')
        )

        self.assertIn(
            'Not Found',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
