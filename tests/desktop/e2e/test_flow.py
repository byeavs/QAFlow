import time
import allure
import pytest
import requests
from playwright.sync_api import expect

pytestmark = pytest.mark.e2e

SAUCE_URL = "https://www.saucedemo.com"
REQRES_URL = "https://reqres.in/api"
HTTPBIN_URL = "https://httpbin.org"


@allure.title("E2E: Login → Add to Cart → Checkout")
@allure.severity(allure.severity_level.BLOCKER)
def test_full_purchase_flow(logged_in_sauce):
    inv = logged_in_sauce["inventory"]
    cart = logged_in_sauce["cart"]
    checkout = logged_in_sauce["checkout"]
    page = logged_in_sauce["page"]

    with allure.step("Добавить первый товар в корзину"):
        inv.add_first_item()
        assert inv.get_cart_count() == "1"

    with allure.step("Перейти в корзину"):
        inv.go_to_cart()
        expect(page).to_have_url(f"{SAUCE_URL}/cart.html")

    with allure.step("В корзине 1 товар"):
        assert cart.get_item_count() == 1

    with allure.step("Перейти к оформлению"):
        cart.proceed_to_checkout()
        expect(page).to_have_url(f"{SAUCE_URL}/checkout-step-one.html")

    with allure.step("Заполнить данные доставки"):
        checkout.fill_info("QA", "Bot", "12345")
        checkout.continue_checkout()
        expect(page).to_have_url(f"{SAUCE_URL}/checkout-step-two.html")

    with allure.step("Завершить заказ"):
        checkout.finish()
        expect(page).to_have_url(f"{SAUCE_URL}/checkout-complete.html")

    with allure.step("Подтверждение заказа"):
        assert "Thank you" in checkout.get_confirmation_text()


@allure.title("E2E: Несколько невалидных попыток логина")
@allure.severity(allure.severity_level.CRITICAL)
def test_negative_login_flow(sauce_pages, page):
    login = sauce_pages["login"]
    cases = [
        ("", "secret_sauce"),
        ("standard_user", ""),
        ("invalid", "invalid"),
    ]

    with allure.step("Открыть страницу логина"):
        login.open()

    for username, password in cases:
        with allure.step(f"Попытка: user='{username}' pass='{password}'"):
            login.login(username, password)
            assert login.is_error_visible(), f"Ожидалась ошибка для {username}/{password}"
            login.close_error()


@allure.title("E2E: API консистентность — структура пользователей")
@allure.severity(allure.severity_level.NORMAL)
def test_api_data_consistency():
    with allure.step("Получить список пользователей через API"):
        r = requests.get(f"{REQRES_URL}/users", params={"page": 1})
        assert r.status_code == 200

    with allure.step("Проверить структуру каждого пользователя"):
        users = r.json()["data"]
        assert len(users) > 0
        for u in users:
            assert "id" in u
            assert "@" in u["email"]
            assert u["first_name"]
            assert u["last_name"]

    with allure.step("Пагинация корректна"):
        meta = r.json()
        assert meta["total"] > 0
        assert meta["total_pages"] >= 1


@allure.title("E2E: httpbin delay — ответ в пределах таймаута")
@allure.severity(allure.severity_level.MINOR)
def test_httpbin_delay():
    with allure.step("GET /delay/2 — ждём ответа"):
        start = time.time()
        r = requests.get(f"{HTTPBIN_URL}/delay/2", timeout=10)
        elapsed = time.time() - start

    with allure.step("Статус 200"):
        assert r.status_code == 200

    with allure.step("Задержка ~2 секунды (не более 8)"):
        assert elapsed >= 2.0
        assert elapsed < 8.0

    with allure.step("Тело ответа содержит url и headers"):
        body = r.json()
        assert "url" in body
        assert "headers" in body
