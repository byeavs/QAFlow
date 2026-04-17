from playwright.sync_api import Page, expect
from tests.mobile.pages.base_page import BasePage


class MobileInventoryPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.inventory_list = page.locator(".inventory_list")
        self.inventory_items = page.locator(".inventory_item")
        self.cart_badge = page.locator(".shopping_cart_badge")
        self.cart_link = page.locator(".shopping_cart_link")
        self.add_buttons = page.locator(".inventory_item button")
        self.burger_menu = page.locator("#react-burger-menu-btn")
        self.nav_menu = page.locator(".bm-menu-wrap")
        self.sort_dropdown = page.locator("[data-test='product-sort-container']")
        self.item_names = page.locator(".inventory_item_name")
        self.item_prices = page.locator(".inventory_item_price")

    def is_loaded(self) -> bool:
        return self.inventory_list.is_visible()

    def get_item_count(self) -> int:
        return self.inventory_items.count()

    def add_first_item(self):
        self.add_buttons.first.click()

    def get_cart_count(self) -> str:
        return self.cart_badge.inner_text()

    def open_burger_menu(self):
        self.burger_menu.click()
        expect(self.nav_menu).to_be_visible()

    def go_to_cart(self):
        self.cart_link.click()

    def sort_by(self, value: str):
        self.sort_dropdown.select_option(value)

    def assert_adaptive_layout(self):
        expect(self.inventory_list).to_be_visible()
        expect(self.cart_link).to_be_visible()
        expect(self.burger_menu).to_be_visible()
        items = self.inventory_items.all()
        assert len(items) > 0
