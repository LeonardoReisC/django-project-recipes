from django.core.exceptions import ValidationError

import re


def add_attr(field, attr_name, attr_new_value):
    field.widget.attrs[attr_name] = attr_new_value


def add_placeholder(field, placeholder_value):
    add_attr(field, 'placeholder', placeholder_value)


def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError(
            (
                'Invalid password. '
                'Please ensure it meets the minimum requirements.'
            ),
            code='invalid',
        )
