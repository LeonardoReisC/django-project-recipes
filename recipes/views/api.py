from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from recipes.models import Recipe
from recipes.serializer import RecipeSerializer
from tag.models import Tag
from tag.serializer import TagSerializer


class RecipeAPUV2Pagination(PageNumberPagination):
    page_size = 1


class RecipeAPIV2List(ListCreateAPIView):
    queryset = Recipe.objects.get_published()
    serializer_class = RecipeSerializer
    pagination_class = RecipeAPUV2Pagination


class RecipeAPIV2Detail(APIView):
    def get_recipe(self, pk):
        return get_object_or_404(Recipe.objects.get_published(), pk=pk)

    def get(self, request, pk):
        recipe = self.get_recipe(pk)
        serializer = RecipeSerializer(
            instance=recipe,
            context={
                'request': request
            }
        )
        return Response(serializer.data)

    def patch(self, request, pk):
        recipe = self.get_recipe(pk)
        recipe = get_object_or_404(Recipe.objects.get_published(), pk=pk)
        serializer = RecipeSerializer(
            instance=recipe,
            data=request.data,
            context={
                'request': request
            },
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        recipe = self.get_recipe(pk)
        recipe = get_object_or_404(Recipe.objects.get_published(), pk=pk)
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view()
def tag_api_detail(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    serializer = TagSerializer(instance=tag)

    return Response(serializer.data)
