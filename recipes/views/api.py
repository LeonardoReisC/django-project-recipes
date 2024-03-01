from unicodedata import category

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from recipes.models import Recipe
from recipes.serializer import RecipeSerializer
from tag.models import Tag
from tag.serializer import TagSerializer


@api_view(http_method_names=['get', 'post'])
def recipe_api_list(request):
    if request.method == 'GET':
        recipes = Recipe.objects.get_published()[:10]
        serializer = RecipeSerializer(
            instance=recipes,
            many=True,
            context={
                'request': request
            }
        )

        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = RecipeSerializer(
            data=request.data,
            context={
                'request': request
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(
            author_id=1,
            category_id=1,
            tags=[1, 2],

        )
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


@api_view()
def recipe_api_detail(request, pk):
    recipe = get_object_or_404(Recipe.objects.get_published(), pk=pk)
    serializer = RecipeSerializer(
        instance=recipe,
        context={
            'request': request
        }
    )

    return Response(serializer.data)


@api_view()
def tag_api_detail(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    serializer = TagSerializer(instance=tag)

    return Response(serializer.data)
