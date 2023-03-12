import unittest

from base.webdriverfactory import WebDriverFactory
from config_files import utils
from pages.home.login_page import LoginPage

class TcTempl(unittest.TestCase):

    def setup_method(self, method):
        self.getDriver()

    def teardown_method(self, method):
        self.closeDriver()

    def getDriver(self):
        wdf = WebDriverFactory(utils.BROWSER)
        self.driver = wdf.getWebDriverInstance()

    def closeDriver(self):
        self.driver.close()

    def login_user(self, user):
        self.lp = LoginPage(self.driver)
        self.lp.login(user.get("login"), user.get("password"))

    def logout_user(self):
        self.lp = LoginPage(self.driver)
        self.lp.logout()

