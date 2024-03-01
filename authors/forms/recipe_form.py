from collections import defaultdict

from django import forms
from authors.validator import RecipeValidator

from recipes.models import Recipe
from utils.django_forms import add_attr


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

    def clean(self, *args, **kwargs):
        cleaned_data = super().clean(*args, **kwargs)

        RecipeValidator(cleaned_data)

        return cleaned_data
