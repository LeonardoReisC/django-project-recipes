from selenium.webdriver.common.by import By
import pytest

from .base import AuthorsBaseFunctionalTest


@pytest.mark.functional_tests
class AuthorsRegisterFunctionalTest(AuthorsBaseFunctionalTest):

    def fill_form_with_valid_data(self, form, **fields):
        data = {
            'first_name': 'user_first',
            'last_name': 'user_last',
            'username': 'user_username',
            'email': 'user@email.com',
            'password': 'user_P@ssw0rd',
            'password_confirm': 'user_P@ssw0rd',
            **fields
        }

        fields = form.find_elements(By.TAG_NAME, 'input')
        for field in fields:
            if field.is_displayed():
                name = field.get_attribute('name')
                field.send_keys(data[name])

    def get_form(self):
        return self.browser.find_element(
            By.XPATH,
            '/html/body/main/div[2]/form'
        )

    def update_filled_form(self, callback=None, **fields):
        self.browser.get(self.live_server_url + '/authors/register/')
        form = self.get_form()

        self.fill_form_with_valid_data(form, **fields)

        if callback is not None:
            callback(form)
        return form

    def test_authors_first_name_field_shows_error_message_if_empty(self):
        def callback(form):
            form.submit()
            form = self.get_form()
            self.assertIn('Write your first name.', form.text)

        self.update_filled_form(callback, first_name=' ')

    def test_authors_last_name_field_shows_error_message_if_empty(self):
        def callback(form):
            form.submit()
            form = self.get_form()
            self.assertIn('Write your last name.', form.text)

        self.update_filled_form(callback, last_name=' ')

    def test_authors_username_field_shows_error_message_if_empty(self):
        def callback(form):
            form.submit()
            form = self.get_form()
            self.assertIn('This field must not be empty.', form.text)

        self.update_filled_form(callback, username=' ' * 4)

    def test_authors_email_field_shows_error_message_if_invalid(self):
        def callback(form):
            form.submit()
            form = self.get_form()
            self.assertIn('Enter a valid email address.', form.text)

        self.update_filled_form(callback, email='user@invalid')

    def test_authors_password_fields_shows_error_message_if_no_match(self):
        def callback(form):
            form.submit()
            form = self.get_form()
            self.assertIn('Must be equal to password.', form.text)

        self.update_filled_form(callback, password_confirm=' ')

    def test_user_valid_data_register_successfully(self):
        def callback(form):
            form.submit()
            self.assertIn(
                'User successfully created, please log in.',
                self.browser.find_element(By.TAG_NAME, 'body').text
            )
        self.update_filled_form(callback)
