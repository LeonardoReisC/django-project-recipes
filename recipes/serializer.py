from rest_framework import serializers

from authors.validator import RecipeValidator
from recipes.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'description',
            'preparation', 'preparation_time', 'preparation_time_unit',
            'servings', 'servings_unit', 'cover',
            'preparation_steps', 'author', 'category',
            'tags', 'public'
        ]

    public = serializers.BooleanField(source='is_published', read_only=True)
    preparation = serializers.SerializerMethodField(read_only=True)
    category = serializers.StringRelatedField(read_only=True)
    tags = serializers.HyperlinkedRelatedField(
        view_name='recipes:recipes_api_v2_tag',
        many=True,
        read_only=True,
    )

    def get_preparation(self, recipe):
        return f'{recipe.preparation_time} {recipe.preparation_time_unit}'

    def validate(self, attrs):
        if self.instance is not None and attrs.get('title') is None:
            attrs['title'] = self.instance.title

        if self.instance is not None and attrs.get('preparation_time') is None:
            attrs['preparation_time'] = self.instance.preparation_time

        if self.instance is not None and attrs.get('servings') is None:
            attrs['servings'] = self.instance.servings

        validated_data = super().validate(attrs)

        RecipeValidator(
            validated_data,
            error_class=serializers.ValidationError
        )

        return validated_data
