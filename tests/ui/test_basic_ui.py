import allure
import pytest
from playwright.sync_api import Page, expect

pytestmark = pytest.mark.ui

BASE = "https://the-internet.herokuapp.com"


@allure.title("Checkbox — переключение состояния")
@allure.severity(allure.severity_level.NORMAL)
def test_checkbox_toggle(page: Page):
    with allure.step("Открыть /checkboxes"):
        page.goto(f"{BASE}/checkboxes")

    with allure.step("Запомнить начальное состояние"):
        cb = page.locator("input[type='checkbox']").first
        initial = cb.is_checked()

    with allure.step("Кликнуть чекбокс"):
        cb.click()

    with allure.step("Состояние изменилось"):
        assert cb.is_checked() != initial


@allure.title("Dropdown — выбор опций")
@allure.severity(allure.severity_level.NORMAL)
def test_dropdown_select(page: Page):
    with allure.step("Открыть /dropdown"):
        page.goto(f"{BASE}/dropdown")

    with allure.step("Выбрать Option 1"):
        page.select_option("#dropdown", value="1")
        expect(page.locator("#dropdown option:checked")).to_have_text("Option 1")

    with allure.step("Выбрать Option 2"):
        page.select_option("#dropdown", value="2")
        expect(page.locator("#dropdown option:checked")).to_have_text("Option 2")


@allure.title("Главная страница — h1 виден")
@allure.severity(allure.severity_level.MINOR)
def test_home_heading(page: Page):
    with allure.step("Открыть главную"):
        page.goto(BASE)

    with allure.step("h1 содержит 'Welcome'"):
        expect(page.locator("h1")).to_contain_text("Welcome to the-internet")


@allure.title("Add/Remove Elements — добавление и удаление")
@allure.severity(allure.severity_level.NORMAL)
def test_add_remove_elements(page: Page):
    with allure.step("Открыть /add_remove_elements/"):
        page.goto(f"{BASE}/add_remove_elements/")

    with allure.step("Добавить элемент"):
        page.click("button:text('Add Element')")
        expect(page.locator("button:text('Delete')")).to_be_visible()

    with allure.step("Удалить элемент"):
        page.click("button:text('Delete')")
        expect(page.locator("button:text('Delete')")).not_to_be_visible()
