from base.basepage import BasePage


class LoginPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # locators
    _login_button = ".ico-login"
    _confirm_log_in_button = ".ico-register"
    _email_field = "Email"
    _password_field = "Password"
    _logout_button = ".ico-logout"

    def click_login_button(self):
        self.elementClick(self._login_button, locatorType="css")
        return self

    def enter_email(self, email):
        self.sendKeys(email, self._email_field, locatorType="id")
        return self

    def enter_password(self, password):
        self.sendKeys(password, self._password_field, locatorType="id")
        return self

    def confirm_login(self):
        self.elementClick(self._confirm_log_in_button, locatorType="id")
        return self

    def login(self, email="", password=""):
        self.click_login_button(). \
            enter_email(email). \
            enter_password(password). \
            confirm_login()

        return self.isElementPresent("div[class='header-links'] a[class='account']",
                                     locatorType="css")

    def verifyLoginTitle(self):
        return self.verifyPageTitle("")

    def logout(self):
        self.elementClick(self._logout_button, locatorType="css")