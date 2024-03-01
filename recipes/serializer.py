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
        validated_data = super().validate(attrs)

        RecipeValidator(
            validated_data,
            error_class=serializers.ValidationError
        )

        return validated_data
