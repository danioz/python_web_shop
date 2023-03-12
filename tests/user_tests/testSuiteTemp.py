import unittest
from tests.user_tests.login_user_tests import LoginTests


tc1 = LoginTests.test_1_positive_login

smokeTest = unittest.TestSuite([tc1])

unittest.TextTestRunner(verbosity=1).run(smokeTest)