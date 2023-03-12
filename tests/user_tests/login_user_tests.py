import pytest

from config_files import utils
from pages.home.login_page import LoginPage
from tests.tc_template import TcTempl


class LoginTests(TcTempl):
    @pytest.mark.run(order=1)
    def test_1_positive_login(self):
        self.login_user(utils.USER1)
        loginPage = LoginPage(self.driver)
        loginPage.verifyLoginName(utils.USER1.get("login"))

    @pytest.mark.run(order=2)
    def test_2_(self):
        None

    @pytest.mark.run(order=3)
    def test_3_(self):
        None
