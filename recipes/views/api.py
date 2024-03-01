from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from recipes.models import Recipe
from recipes.serializer import RecipeSerializer
from tag.models import Tag
from tag.serializer import TagSerializer


class RecipeAPUV2Pagination(PageNumberPagination):
    page_size = 1


class RecipeAPIV2ViewSet(ModelViewSet):
    queryset = Recipe.objects.get_published()
    serializer_class = RecipeSerializer
    pagination_class = RecipeAPUV2Pagination


@api_view()
def tag_api_detail(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    serializer = TagSerializer(instance=tag)

    return Response(serializer.data)
