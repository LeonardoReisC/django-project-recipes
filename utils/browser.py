from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from pathlib import Path
import os

ROOT_PATH = Path(__file__).parent.parent
CHROMEDRIVER_NAME = 'chromedriver.exe'
CHROMEDRIVER_PATH = ROOT_PATH / 'bin' / CHROMEDRIVER_NAME


def make_chrome_browser(*options):
    chrome_options = webdriver.ChromeOptions()
    if options is not None:
        for option in options:
            chrome_options.add_argument(option)

    if os.environ.get('SELENIUM_HEADLESS') == '1':
        chrome_options.add_argument('--headless')

    chrome_service = Service(executable_path=CHROMEDRIVER_PATH)
    return webdriver.Chrome(service=chrome_service, options=chrome_options)


if __name__ == '__main__':
    browser = make_chrome_browser()
    browser.get('https://github.com/LeonardoReisC')
    browser.quit()
