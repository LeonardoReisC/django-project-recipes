from rest_framework import serializers

from recipes.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'description',
            'preparation', 'author', 'category',
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
