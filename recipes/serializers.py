from django.contrib.auth.models import User
from rest_framework import serializers

from tag.models import Tag


class RecipeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=65)
    description = serializers.CharField(max_length=165)
    public = serializers.BooleanField(source='is_published')
    preparation = serializers.SerializerMethodField()
    category = serializers.StringRelatedField()
    author = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
    )
    tags = serializers.HyperlinkedRelatedField(
        queryset=Tag.objects.all(),
        view_name='recipes:recipes_api_v2_tag',
        many=True,
    )

    def get_preparation(self, recipe):
        return f'{recipe.preparation_time} {recipe.preparation_time_unit}'
