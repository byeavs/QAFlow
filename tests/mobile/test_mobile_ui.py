import allure
import pytest
from playwright.sync_api import expect

pytestmark = pytest.mark.mobile

SAUCE_URL = "https://www.saucedemo.com"

EXPECTED_WIDTHS = {
    "Pixel 5": 393,
    "iPhone 13": 390,
}


@allure.title("Адаптивный UI — ширина viewport соответствует устройству [{device_name}]")
@allure.severity(allure.severity_level.CRITICAL)
def test_viewport_width_matches_device(login_page, device_name):
    with allure.step(f"Открыть страницу на {device_name}"):
        login_page.open()

    with allure.step("Проверить ширину viewport"):
        viewport = login_page.get_viewport()
        expected_width = EXPECTED_WIDTHS[device_name]

        assert viewport["width"] == expected_width, (
            f"{device_name}: ожидался width={expected_width}, "
            f"получен {viewport['width']}"
        )

    with allure.step("Viewport мобильный (width <= 768)"):
        assert login_page.is_mobile_viewport()


@allure.title("Адаптивный UI — элементы инвентаря видны [{device_name}]")
@allure.severity(allure.severity_level.CRITICAL)
def test_inventory_adaptive_layout(logged_in_mobile, device_name):
    with allure.step(f"Проверить адаптивную верстку инвентаря [{device_name}]"):
        logged_in_mobile.assert_adaptive_layout()

    with allure.step("Бургер-меню присутствует (мобильная навигация)"):
        expect(logged_in_mobile.burger_menu).to_be_visible()

    with allure.step("Корзина доступна"):
        expect(logged_in_mobile.cart_link).to_be_visible()


@allure.title("Адаптивный UI — title страницы корректен [{device_name}]")
@allure.severity(allure.severity_level.MINOR)
def test_page_title_on_mobile(login_page, device_name):
    with allure.step(f"Открыть SauceDemo на {device_name}"):
        login_page.open()

    with allure.step("Title = 'Swag Labs'"):
        assert login_page.get_title() == "Swag Labs"

    with allure.step("Логотип виден на мобильном"):
        expect(login_page.logo).to_be_visible()


@allure.title("Адаптивный UI — имена и цены товаров видны [{device_name}]")
@allure.severity(allure.severity_level.NORMAL)
def test_product_info_visible_on_mobile(logged_in_mobile, device_name):
    with allure.step(f"Проверить отображение товаров на {device_name}"):
        expect(logged_in_mobile.item_names.first).to_be_visible()
        expect(logged_in_mobile.item_prices.first).to_be_visible()

    with allure.step("Кнопка добавления в корзину доступна"):
        expect(logged_in_mobile.add_buttons.first).to_be_visible()
