import allure
import pytest
from playwright.sync_api import expect

pytestmark = pytest.mark.mobile

SAUCE_URL = "https://www.saucedemo.com"


@allure.title("Навигация — бургер-меню открывается [{device_name}]")
@allure.severity(allure.severity_level.CRITICAL)
def test_burger_menu_opens(logged_in_mobile, mobile_page, device_name):
    with allure.step(f"Проверить что мы на inventory [{device_name}]"):
        expect(mobile_page).to_have_url(f"{SAUCE_URL}/inventory.html")

    with allure.step("Открыть бургер-меню"):
        logged_in_mobile.open_burger_menu()

    with allure.step("Меню отображается"):
        expect(logged_in_mobile.nav_menu).to_be_visible()


@allure.title("Навигация — переход в корзину [{device_name}]")
@allure.severity(allure.severity_level.CRITICAL)
def test_navigate_to_cart(logged_in_mobile, mobile_page, device_name):
    with allure.step(f"Добавить товар в корзину [{device_name}]"):
        logged_in_mobile.add_first_item()
        assert logged_in_mobile.get_cart_count() == "1"

    with allure.step("Перейти в корзину"):
        logged_in_mobile.go_to_cart()

    with allure.step("URL изменился на /cart.html"):
        expect(mobile_page).to_have_url(f"{SAUCE_URL}/cart.html")


@allure.title("Навигация — сортировка товаров [{device_name}]")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize("sort_value,label", [
    ("az", "A→Z"),
    ("za", "Z→A"),
    ("lohi", "цена по возрастанию"),
    ("hilo", "цена по убыванию"),
])
def test_sort_products(logged_in_mobile, device_name, sort_value, label):
    with allure.step(f"Сортировать товары: {label} [{device_name}]"):
        logged_in_mobile.sort_by(sort_value)

    with allure.step("Товары отображаются после сортировки"):
        assert logged_in_mobile.get_item_count() > 0

    with allure.step("Дропдаун сортировки виден"):
        expect(logged_in_mobile.sort_dropdown).to_be_visible()


@allure.title("Навигация — количество товаров на странице [{device_name}]")
@allure.severity(allure.severity_level.NORMAL)
def test_inventory_item_count(logged_in_mobile, device_name):
    with allure.step(f"Проверить каталог товаров [{device_name}]"):
        count = logged_in_mobile.get_item_count()

    with allure.step("На странице 6 товаров (стандартный каталог)"):
        assert count == 6, f"Ожидалось 6 товаров, получено {count}"
