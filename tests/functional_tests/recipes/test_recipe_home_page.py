from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from unittest.mock import patch
import pytest

from .base import RecipeBaseFunctionalTest
from recipes.tests.test_recipe_base import RecipeMixin


@pytest.mark.functional_tests
class RecipeHomePageFunctionTest(RecipeBaseFunctionalTest, RecipeMixin):

    def test_recipe_home_page_shows_not_found_message_when_no_recipes(self):
        self.browser.get(self.live_server_url)

        text = 'No recipes found here D:'
        body = self.browser.find_element(By.TAG_NAME, 'body')

        self.assertIn(text, body.text)

    @patch('recipes.views.PER_PAGE', new=3)
    def test_recipe_search_input_find_the_correct_recipes(self):
        recipes = self.make_recipes_in_batch()

        title_needed = 'Test Recipe Title'
        recipes[0].title = title_needed
        recipes[0].save()

        # Open the page
        self.browser.get(self.live_server_url)

        # See a search field with placeholder "Search for a recipe"
        search_input = self.browser.find_element(
            By.XPATH,
            '//input[@placeholder="Search for a recipe"]'
        )

        # Click on the input and type the recipe title
        search_input.send_keys(title_needed)
        search_input.send_keys(Keys.ENTER)

        # User see the result he was looking for
        self.assertIn(
            title_needed,
            self.browser.find_element(By.TAG_NAME, 'main').text
        )
