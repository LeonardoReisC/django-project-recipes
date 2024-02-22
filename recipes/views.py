from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
from django.db.models.fields.files import ImageFieldFile
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.http.response import Http404
from django.shortcuts import render
from django.views.generic import DetailView, ListView
import os

from utils.pagination import make_pagination
from .models import Recipe

PER_PAGE = int(os.environ.get('PER_PAGE', 3))

# Create your views here.


def theory(request):
    try:
        recipes = Recipe.objects.get(pk=100)
    except ObjectDoesNotExist:
        recipes = None

    return render(
        request,
        'recipes/pages/theory.html',
        context={
            'recipes': recipes
        }
    )


class RecipeListViewBase(ListView):
    model = Recipe
    context_object_name = 'recipes'
    paginate_by = None
    ordering = ['-id']
    template_name = 'recipes/pages/home.html'

    def get_queryset(self, *args, **kwargs):
        query_set = super().get_queryset(*args, **kwargs)
        query_set = query_set.filter(is_published=True)

        query_set = query_set.select_related('author', 'category')

        return query_set

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        page_obj, pagination_range = make_pagination(
            self.request,
            context.get('recipes'),
            PER_PAGE
        )

        context.update({
            'recipes': page_obj,
            'pagination_range': pagination_range,
        })

        return context


class RecipeListViewHome(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'


class RecipeListViewHomeApi(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'

    def render_to_response(self, context, **response_kwargs):
        recipes = self.get_context_data().get('recipes').object_list.values()

        return JsonResponse(list(recipes), safe=False)


class RecipeListViewCategory(RecipeListViewBase):
    template_name = 'recipes/pages/category.html'

    def get_queryset(self, *args, **kwargs):
        query_set = super().get_queryset(*args, **kwargs)
        query_set = query_set.filter(
            category_id=self.kwargs.get('category_id')
        )

        if not query_set:
            raise Http404()

        return query_set

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update({
            'title': (
                f'{context.get("recipes")[0].category.name} - Category | '
            ),
        })

        return context


class RecipeListViewSearch(RecipeListViewBase):
    template_name = 'recipes/pages/search.html'

    def get_queryset(self, *args, **kwargs):
        query_set = super().get_queryset(*args, **kwargs)
        search_term = self.request.GET.get('q', '').strip()

        if not search_term:
            raise Http404()

        query_set = query_set.filter(
            Q(
                Q(title__icontains=search_term) |
                Q(description__icontains=search_term)
            )
        )

        return query_set

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        search_term = self.request.GET.get('q', '').strip()

        context.update({
            'title': f'Search for "{search_term}" | ',
            'search_term': search_term,
            'additional_url_query': f'&q={search_term}',
        })

        return context


class RecipeDetailView(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipes/pages/recipe-view.html'

    def get_queryset(self, *args, **kwargs):
        query_set = super().get_queryset(*args, **kwargs)
        query_set = query_set.filter(is_published=True)

        return query_set

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context.update({
            'is_detail_page': True,
        })

        return context


class RecipeDetailViewApi(RecipeDetailView):
    class RecipeEncoder(DjangoJSONEncoder):
        def __init__(self, request, **kwargs) -> None:
            super().__init__(**kwargs)
            self.request = request

        def default(self, o):
            if isinstance(o, ImageFieldFile):
                return self.request.get_host() + o.url

            return super().default(o)

    def render_to_response(self, context, **response_kwargs):
        recipe_model = self.get_context_data().get('recipe')
        recipe_dict = model_to_dict(
            recipe_model,
            exclude=['is_published', 'preparation_steps_is_html']
        )

        recipe_dict.update({
            'created_at': recipe_model.created_at,
            'updated_at': recipe_model.updated_at,
        })

        return JsonResponse(
            recipe_dict,
            encoder=self.RecipeEncoder,
            safe=False,
            json_dumps_params={
                'indent': 2,
                'request': self.request,
            }
        )
