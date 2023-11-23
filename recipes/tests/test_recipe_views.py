from django.urls import reverse, resolve

from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipeViewsTest(RecipeTestBase):
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(
            reverse('recipes:home')
        )
        self.assertIs(view.func, views.home)

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

    def test_recipe_category_view_function_is_correct(self):
        view = resolve(
            reverse('recipes:category', kwargs={'category_id': 1})
        )
        self.assertIs(view.func, views.category)

    def test_recipe_category_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1000})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_template_loads_recipes(self):
        tested_title = 'This is a category test'

        # needs a recipe for this test
        self.make_recipe(title=tested_title)

        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1})
        )
        content = response.content.decode('utf-8')

        self.assertIn(tested_title, content)

    def test_recipe_category_template_do_not_load_recipes_not_published(self):
        # needs a recipe for this test
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(
            reverse(
                'recipes:category',
                kwargs={'category_id': recipe.category.id}
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(
            reverse('recipes:recipe', kwargs={'id': 1000})
        )
        self.assertIs(view.func, views.recipe)

    def test_recipe_detail_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1000})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_template_loads_the_correct_recipes(self):
        tested_title = 'This is a detail page - It loads one recipe'

        # needs a recipe for this test
        self.make_recipe(title=tested_title)

        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1})
        )
        content = response.content.decode('utf-8')

        self.assertIn(tested_title, content)

    def test_recipe_detail_template_do_not_load_recipe_not_published(self):
        # needs a recipe for this test
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(
            reverse(
                'recipes:recipe',
                kwargs={'id': recipe.id}
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_recipe_search_uses_correct_view_function(self):
        url = reverse('recipes:search')
        resolved = resolve(url)

        self.assertIs(resolved.func, views.search)

    def test_recipe_search_loads_correct_template(self):
        url = reverse('recipes:search') + '?q=test'
        response = self.client.get(url)

        self.assertTemplateUsed(response, 'recipes/pages/search.html')

    def test_recipe_search_raises_404_if_no_search_term(self):
        url = reverse('recipes:search')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
