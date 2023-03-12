import pytest

from config_files import utils
from tests.tc_template import TcTempl


class LoginTests(TcTempl):
    @pytest.mark.run(order=1)
    def test_1_possitive_login(self):
        self.login_user(utils.USER1)

    @pytest.mark.run(order=2)
    def test_2_(self):
        None

    @pytest.mark.run(order=3)
    def test_3_(self):
        None
