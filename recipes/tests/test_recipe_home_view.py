from django.urls import reverse, resolve
from unittest.mock import patch

from recipes.views import site
from .test_recipe_base import RecipeTestBase


class RecipeHomeViewTest(RecipeTestBase):
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(
            reverse('recipes:home')
        )
        self.assertIs(view.func.view_class, site.RecipeListViewHome)

    def test_recipe_home_view_returns_status_code_200_OK(self):
        response = self.client.get(
            reverse('recipes:home')
        )
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(
            reverse('recipes:home')
        )
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get(
            reverse('recipes:home')
        )
        self.assertIn(
            'No recipes found',
            response.content.decode('utf-8')
        )

    def test_recipe_home_template_loads_recipes(self):
        # needs a recipe for this test
        recipe = self.make_recipe()

        response = self.client.get(
            reverse('recipes:home')
        )
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']

        # check if template contains the recipe title
        self.assertIn(recipe.title, content)

        # check if one recipe exists
        self.assertEqual(len(response_context_recipes), 1)

    def test_recipe_home_template_do_not_load_recipes_not_published(self):
        # needs a recipe for this test
        self.make_recipe(is_published=False)

        response = self.client.get(
            reverse('recipes:home')
        )
        content = response.content.decode('utf-8')

        self.assertIn(
            'No recipes found',
            content,
        )

    @patch('recipes.views.site.PER_PAGE', new=3)
    def test_recipe_home_is_paginated(self):
        self.make_recipes_in_batch(8)

        response = self.client.get(reverse('recipes:home'))
        recipes = response.context['recipes']
        paginator = recipes.paginator

        self.assertEqual(paginator.num_pages, 3)
        self.assertEqual(len(paginator.get_page(1)), 3)
        self.assertEqual(len(paginator.get_page(2)), 3)
        self.assertEqual(len(paginator.get_page(3)), 2)

    @patch('recipes.views.site.PER_PAGE', new=3)
    def test_invalid_page_query_uses_page_one(self):
        response = self.client.get(reverse('recipes:home') + '?page=*')
        self.assertEqual(response.context['recipes'].number, 1)
