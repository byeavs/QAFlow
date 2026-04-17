from playwright.sync_api import Page, expect
from tests.mobile.pages.base_page import BasePage

URL = "https://www.saucedemo.com"


class MobileLoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.username_input = page.locator("#user-name")
        self.password_input = page.locator("#password")
        self.login_button = page.locator("#login-button")
        self.error_message = page.locator("[data-test='error']")
        self.error_close = page.locator(".error-button")
        self.logo = page.locator(".login_logo")

    def open(self):
        self.navigate(URL)

    def login(self, username: str, password: str):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def get_error(self) -> str:
        return self.error_message.inner_text()

    def is_error_visible(self) -> bool:
        return self.error_message.is_visible()

    def close_error(self):
        self.error_close.click()

    def assert_login_form_visible(self):
        expect(self.username_input).to_be_visible()
        expect(self.password_input).to_be_visible()
        expect(self.login_button).to_be_visible()
        expect(self.logo).to_be_visible()
