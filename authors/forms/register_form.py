from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from utils.django_forms import add_placeholder, strong_password


class RegisterForm(forms.ModelForm):
    first_name = forms.CharField(
        error_messages={
            'required': 'Write your first name.'
        },
        label='First name'
    )

    last_name = forms.CharField(
        error_messages={
            'required': 'Write your last name.'
        },
        label='Last name'
    )

    username = forms.CharField(
        error_messages={
            'required': 'This field must not be empty.',
            'min_length': 'Username must have at least 4 characters.',
            'max_length': 'Username must have less than 150 characters.',
        },
        help_text='Must have between 4 and 150 characters.',
        min_length=4,
        max_length=150,
        label='Username',
    )

    email = forms.EmailField(
        error_messages={
            'required': 'This field must not be empty.'
        },
        help_text='This e-mail must be valid.',
        label='E-mail'
    )

    password = forms.CharField(
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'This field must not be empty.'
        },
        help_text=(
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        ),
        validators=[strong_password],
        label='Password',
    )

    password_confirm = forms.CharField(
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'This field must not be empty.'
        },
        label='Confirm your password',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['first_name'], 'e.g. Leonardo')
        add_placeholder(self.fields['last_name'], 'e.g. Reis')
        add_placeholder(self.fields['username'], 'Type your username here')
        add_placeholder(self.fields['email'], 'Type your e-mail here')
        add_placeholder(self.fields['password'], 'Type your password here')
        add_placeholder(
            self.fields['password_confirm'],
            'Type your password here again'
        )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()

        if (exists):
            raise ValidationError(
                "User email is already in use.",
                code='invalid',
            )

        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password != password_confirm:
            raise ValidationError({
                'password_confirm': ValidationError(
                    'Must be equal to password.',
                    code='invalid',
                ),
            })
