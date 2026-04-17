from playwright.sync_api import Page
from .base_page import BasePage

URL = "https://www.saucedemo.com/inventory.html"


class InventoryPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.inventory_list = page.locator(".inventory_list")
        self.cart_badge = page.locator(".shopping_cart_badge")
        self.cart_link = page.locator(".shopping_cart_link")
        self.items = page.locator(".inventory_item")
        self.add_buttons = page.locator(".inventory_item button")

    def is_loaded(self) -> bool:
        return self.inventory_list.is_visible()

    def add_first_item(self):
        self.add_buttons.first.click()

    def get_cart_count(self) -> str:
        return self.cart_badge.inner_text()

    def go_to_cart(self):
        self.cart_link.click()
