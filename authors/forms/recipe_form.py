from collections import defaultdict
from django.core.exceptions import ValidationError
from django import forms

from recipes.models import Recipe
from utils.django_forms import add_attr
from utils.strings import is_positive_number


class RecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._my_errors = defaultdict(list)

        add_attr(self.fields['title'], 'class', 'span-2')
        add_attr(self.fields['description'], 'class', 'span-2')
        add_attr(self.fields['preparation_steps'], 'class', 'span-2')
        add_attr(self.fields['cover'], 'class', 'span-2')

    class Meta:
        model = Recipe
        fields = [
            'title',
            'description',
            'preparation_time',
            'preparation_time_unit',
            'servings',
            'servings_unit',
            'preparation_steps',
            'cover',
        ]
        widgets = {
            'preparation_time_unit': forms.Select(
                choices=[
                    ('Minutes', 'Minutes'),
                    ('Hours', 'Hours'),
                ]
            ),
            'servings_unit': forms.Select(
                choices=[
                    ('Portions', 'Portions'),
                    ('Slices', 'Slices'),
                    ('Plates', 'Plates')

                ]
            ),
            'cover': forms.FileInput(
                attrs={
                    'class': 'span-2'
                }
            ),
        }

    def clean_title(self):
        data = self.cleaned_data["title"]

        if len(data) < 5:
            self._my_errors['title'].append('Must have at least 5 characters.')

        return data

    def clean_preparation_time(self):
        data = self.cleaned_data["preparation_time"]

        if not is_positive_number(data):
            self._my_errors['preparation_time'].append(
                'Must be a positive number.'
            )

        return data

    def clean_servings(self):
        data = self.cleaned_data["servings"]

        if not is_positive_number(data):
            self._my_errors['servings'].append(
                'Must be a positive number.'
            )

        return data

    def clean(self, *args, **kwargs):
        cleaned_data = super().clean(*args, **kwargs)

        title = cleaned_data.get('title')
        description = cleaned_data.get('description')

        if title == description:
            self._my_errors['description'].append('Cannot be equal to title.')

        if self._my_errors:
            raise ValidationError(self._my_errors)

        return cleaned_data
