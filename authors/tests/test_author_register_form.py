from parameterized import parameterized
from django.test import TestCase

from authors.forms import RegisterForm


class AuthorRegisterFormUnitTest(TestCase):

    @parameterized.expand([
        ('first_name', 'e.g. Leonardo'),
        ('last_name', 'e.g. Reis'),
        ('username', 'Type your username here'),
        ('email', 'Type your e-mail here'),
        ('password', 'Type your password here'),
        ('password2', 'Type your password here again'),
    ])
    def test_fields_placeholder_is_correct(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']

        self.assertEqual(placeholder, current_placeholder)

    @parameterized.expand([
        ('email', 'This e-mail must be valid.'),
        ('password', (
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        )),
    ])
    def test_fields_help_text_is_correct(self, field, help_text):
        form = RegisterForm()
        current_help_text = form[field].field.help_text

        self.assertEqual(help_text, current_help_text)
