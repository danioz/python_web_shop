from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from config_files.utils import TEST_ENV_URL


class WebDriverFactory():

    def __init__(self, browser):
        self.browser = browser

    def getWebDriverInstance(self):
        if self.browser == "firefox":
            driver = webdriver.Firefox()
        elif self.browser == "chrome":
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        else:
            driver = webdriver.Chrome()
        driver.implicitly_wait(3)
        driver.maximize_window()
        driver.get(TEST_ENV_URL)
        return driver
