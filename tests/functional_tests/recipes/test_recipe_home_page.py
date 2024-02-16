from selenium.webdriver.common.by import By

from .base import RecipeBaseFunctionalTest


class RecipeHomePageFunctionTest(RecipeBaseFunctionalTest):

    def test_recipes_home_page_shows_not_found_message_when_no_recipes(self):
        self.browser.get(self.live_server_url)

        text = 'No recipes found here D:'
        body = self.browser.find_element(By.TAG_NAME, 'body')

        self.assertIn(text, body.text)
