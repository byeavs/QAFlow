from playwright.sync_api import Page
from tests.desktop.ui.pages.base_page import BasePage


class CartPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.cart_items = page.locator(".cart_item")
        self.checkout_button = page.locator("[data-test='checkout']")

    def get_item_count(self) -> int:
        return self.cart_items.count()

    def proceed_to_checkout(self):
        self.checkout_button.click()
