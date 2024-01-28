from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def add_attr(field, attr_name, attr_new_value):
    field.widget.attrs[attr_name] = attr_new_value


def add_placeholder(field, placeholder_value):
    add_attr(field, 'placeholder', placeholder_value)


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Type your password here'
        }),
        error_messages={
            'required': 'This field must not be empty.'
        },
        help_text=(
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        )
    )

    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Type your password here again'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['first_name'], 'e.g. Leonardo')
        add_placeholder(self.fields['last_name'], 'e.g. Reis')
        add_placeholder(self.fields['username'], 'Type your username here')
        add_placeholder(self.fields['email'], 'Type your email here')

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]
        labels = {
            'first_name': 'First name',
            'last_name': 'Last name',
            'username': 'Username',
            'email': 'E-mail',
            'password': 'Password',
        }
        help_texts = {
            'email': 'This e-mail must be valid.'
        }
        error_messages = {
            'username': {
                'required': 'This field must not be empty.'
            }
        }
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Type your first name here'
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Type your password here'
            })
        }

    def clean_first_name(self):
        data = self.cleaned_data.get('first_name').strip()

        if ' ' in data:
            raise ValidationError(
                'Must not have more than 2 names like "%(value)s"',
                code='invalid',
                params={'value': data}
            )

        return data
