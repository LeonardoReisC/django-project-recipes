from collections import defaultdict

from django.core.exceptions import ValidationError

from utils.strings import is_positive_number


class RecipeValidator():
    def __init__(self, data, errors=None, error_class=None):
        self.errors = defaultdict(list) if errors is None else errors
        self.error_class = ValidationError if (
            error_class is None
        ) else error_class
        self.data = data
        self.clean()

    def clean_title(self):
        data = self.data["title"]

        if len(data) < 5:
            self.errors['title'].append('Must have at least 5 characters.')

        return data

    def clean_preparation_time(self):
        data = self.data["preparation_time"]

        if not is_positive_number(data):
            self.errors['preparation_time'].append(
                'Must be a positive number.'
            )

        return data

    def clean_servings(self):
        data = self.data["servings"]

        if not is_positive_number(data):
            self.errors['servings'].append(
                'Must be a positive number.'
            )

        return data

    def clean(self, *args, **kwargs):
        self.clean_title()
        self.clean_preparation_time()
        self.clean_servings()

        data = self.data

        title = data.get('title')
        description = data.get('description')

        if title == description:
            self.errors['description'].append('Cannot be equal to title.')

        if self.errors:
            raise self.error_class(self.errors)
