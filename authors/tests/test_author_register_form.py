from django.test import TestCase as DjangoTestCase
from django.urls import reverse
from parameterized import parameterized
from unittest import TestCase

from authors.forms import RegisterForm


class AuthorRegisterFormUnitTest(TestCase):

    @parameterized.expand([
        ('first_name', 'e.g. Leonardo'),
        ('last_name', 'e.g. Reis'),
        ('username', 'Type your username here'),
        ('email', 'Type your e-mail here'),
        ('password', 'Type your password here'),
        ('password_confirm', 'Type your password here again'),
    ])
    def test_fields_placeholder_is_correct(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']

        self.assertEqual(current_placeholder, placeholder)

    @parameterized.expand([
        ('first_name', ''),
        ('last_name', ''),
        ('username', 'Must have between 4 and 150 characters.'),
        ('email', 'This e-mail must be valid.'),
        ('password', (
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        )),
        ('password_confirm', ''),
    ])
    def test_fields_help_text_is_correct(self, field, help_text):
        form = RegisterForm()
        current_help_text = form[field].field.help_text

        self.assertEqual(current_help_text, help_text)

    @parameterized.expand([
        ('first_name', 'First name'),
        ('last_name', 'Last name'),
        ('username', 'Username'),
        ('email', 'E-mail'),
        ('password', 'Password'),
        ('password_confirm', 'Confirm your password'),
    ])
    def test_fields_label_is_correct(self, field, label):
        form = RegisterForm()
        current_label = form[field].field.label

        self.assertEqual(current_label, label)


class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs) -> None:
        self.form_data = {
            'username': 'user',
            'first_name': 'first',
            'last_name': 'last',
            'email': 'email@anyemail.com',
            'password': 'Str0ngP@ssword',
            'password_confirm': 'Str0ngP@ssword',
        }

        return super().setUp(*args, **kwargs)

    @parameterized.expand([
        ('username', 'This field must not be empty.'),
        ('first_name', 'Write your first name.'),
        ('last_name', 'Write your last name.'),
        ('email', 'This field must not be empty.'),
        ('password', 'This field must not be empty.'),
        ('password_confirm', 'This field must not be empty.'),
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''

        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertIn(msg, response.context['form'].errors.get(field))

    def test_username_field_min_length(self):
        self.form_data['username'] = 'abc'

        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'Username must have at least 4 characters.'
        self.assertIn(msg, response.context['form'].errors.get('username'))

    def test_username_field_max_length(self):
        self.form_data['username'] = '.' * 151

        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'Username must have less than 150 characters.'
        self.assertIn(msg, response.context['form'].errors.get('username'))

    def test_password_field_validator_shows_error_message(self):
        self.form_data['password'] = 'abcd@123'

        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = (
            'Invalid password. '
            'Please ensure it meets the minimum requirements.'
        )
        self.assertIn(msg, response.context['form'].errors.get('password'))

    def test_password_field_validator_is_correct(self):
        self.form_data['password'] = 'Abcd@123'

        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertIsNone(response.context['form'].errors.get('password'))

    def test_password_fieds_must_be_equal(self):
        password = self.form_data['password']
        self.form_data['password_confirm'] = password + '_'

        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'Must be equal to password.'
        self.assertEqual(
            msg, *response.context['form'].errors.get('password_confirm')
        )

    def test_send_get_request_to_registration_create_view_returns_404(self):
        url = reverse('authors:create')
        response = self.client.get(url)
        self.assertEqual(404, response.status_code)

    def test_form_data_is_valid(self):
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        messages = ' '.join(map(
            lambda message: message.message,
            response.context['messages'])
        )
        msg_success = 'Registration complete, user successfully created.'
        self.assertIn(msg_success, messages)
