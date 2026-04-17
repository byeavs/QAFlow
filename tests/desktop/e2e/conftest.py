import pytest
from tests.desktop.ui.pages.login_page import LoginPage
from tests.desktop.ui.pages.inventory_page import InventoryPage
from .pages.cart_page import CartPage
from .pages.checkout_page import CheckoutPage


@pytest.fixture
def sauce_pages(page):
    return {
        "login": LoginPage(page),
        "inventory": InventoryPage(page),
        "cart": CartPage(page),
        "checkout": CheckoutPage(page),
    }


@pytest.fixture
def logged_in_sauce(page):
    lp = LoginPage(page)
    lp.open()
    lp.login("standard_user", "secret_sauce")
    page.wait_for_url("**/inventory.html")
    return {
        "inventory": InventoryPage(page),
        "cart": CartPage(page),
        "checkout": CheckoutPage(page),
        "page": page,
    }
