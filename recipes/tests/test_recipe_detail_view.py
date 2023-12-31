from django.urls import reverse, resolve

from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipeDetailViewTest(RecipeTestBase):
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
