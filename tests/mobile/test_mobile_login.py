import allure
import pytest
from playwright.sync_api import expect

pytestmark = pytest.mark.mobile

SAUCE_URL = "https://www.saucedemo.com"


@allure.title("Мобильный логин — успешная авторизация [{device_name}]")
@allure.severity(allure.severity_level.BLOCKER)
def test_mobile_login_success(login_page, mobile_page, device_name):
    with allure.step(f"Открыть SauceDemo на {device_name}"):
        login_page.open()

    with allure.step("Проверить мобильный viewport"):
        assert login_page.is_mobile_viewport(), (
            f"Ожидался мобильный viewport, получен: {login_page.get_viewport()}"
        )

    with allure.step("Форма логина корректно отображается"):
        login_page.assert_login_form_visible()

    with allure.step("Ввести валидные credentials и войти"):
        login_page.login("standard_user", "secret_sauce")

    with allure.step("Проверить редирект на inventory"):
        expect(mobile_page).to_have_url(f"{SAUCE_URL}/inventory.html")


@allure.title("Мобильный логин — неверный пароль [{device_name}]")
@allure.severity(allure.severity_level.CRITICAL)
def test_mobile_login_wrong_password(login_page, device_name):
    with allure.step(f"Открыть SauceDemo на {device_name}"):
        login_page.open()

    with allure.step("Ввести неверный пароль"):
        login_page.login("standard_user", "wrong_password")

    with allure.step("Ошибка авторизации видна"):
        assert login_page.is_error_visible()
        assert "do not match" in login_page.get_error()


@allure.title("Мобильный логин — пустые поля [{device_name}]")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize("username,password", [
    ("", "secret_sauce"),
    ("standard_user", ""),
    ("", ""),
])
def test_mobile_login_empty_fields(login_page, device_name, username, password):
    with allure.step(f"Открыть страницу на {device_name}"):
        login_page.open()

    with allure.step(f"Попытка логина: user='{username}' pass='{password}'"):
        login_page.login(username, password)

    with allure.step("Ошибка валидации показана"):
        assert login_page.is_error_visible(), "Должна быть ошибка при пустых полях"


@allure.title("Мобильный логин — заблокированный пользователь [{device_name}]")
@allure.severity(allure.severity_level.NORMAL)
def test_mobile_login_locked_user(login_page, device_name):
    with allure.step(f"Открыть SauceDemo на {device_name}"):
        login_page.open()

    with allure.step("Войти как locked_out_user"):
        login_page.login("locked_out_user", "secret_sauce")

    with allure.step("Показана ошибка о блокировке"):
        assert "locked out" in login_page.get_error()
