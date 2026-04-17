import pytest
from tests.desktop.ui.pages.login_page import LoginPage
from tests.desktop.ui.pages.inventory_page import InventoryPage


@pytest.fixture
def login_page(page):
    return LoginPage(page)


@pytest.fixture
def inventory_page(page):
    return InventoryPage(page)


@pytest.fixture
def logged_in(page):
    lp = LoginPage(page)
    lp.open()
    lp.login("standard_user", "secret_sauce")
    page.wait_for_url("**/inventory.html")
    return InventoryPage(page)
