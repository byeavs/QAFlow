import allure
import pytest
from playwright.sync_api import expect

pytestmark = pytest.mark.ui

SAUCE_URL = "https://www.saucedemo.com"


@allure.title("Успешный логин с валидными данными")
@allure.severity(allure.severity_level.BLOCKER)
def test_login_success(login_page, page):
    with allure.step("Открыть SauceDemo"):
        login_page.open()

    with allure.step("Ввести валидные credentials"):
        login_page.login("standard_user", "secret_sauce")

    with allure.step("Проверить редирект на /inventory.html"):
        expect(page).to_have_url(f"{SAUCE_URL}/inventory.html")


@allure.title("Неуспешный логин — неверные credentials")
@allure.severity(allure.severity_level.CRITICAL)
def test_login_failure(login_page):
    with allure.step("Открыть SauceDemo"):
        login_page.open()

    with allure.step("Ввести неверные данные"):
        login_page.login("wrong_user", "wrong_pass")

    with allure.step("Ошибка видна пользователю"):
        assert login_page.is_error_visible()
        assert "do not match" in login_page.get_error()


@allure.title("Логин заблокированного пользователя")
@allure.severity(allure.severity_level.NORMAL)
def test_login_locked_user(login_page):
    with allure.step("Открыть SauceDemo"):
        login_page.open()

    with allure.step("Войти как locked_out_user"):
        login_page.login("locked_out_user", "secret_sauce")

    with allure.step("Показана ошибка о блокировке"):
        assert "locked out" in login_page.get_error()


@allure.title("Заголовок страницы логина корректен")
@allure.severity(allure.severity_level.MINOR)
def test_login_page_title(login_page, page):
    with allure.step("Открыть SauceDemo"):
        login_page.open()

    with allure.step("Title = 'Swag Labs'"):
        expect(page).to_have_title("Swag Labs")

    with allure.step("Логотип виден"):
        expect(login_page.logo).to_be_visible()
