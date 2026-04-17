import allure
import pytest
from playwright.sync_api import sync_playwright, Page

from tests.mobile.pages.login_page import MobileLoginPage
from tests.mobile.pages.inventory_page import MobileInventoryPage

MOBILE_DEVICES = ["Pixel 5", "iPhone 13"]


@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def mobile_browser(playwright_instance):
    browser = playwright_instance.chromium.launch(
        headless=True,
        args=["--no-sandbox", "--disable-dev-shm-usage"],
    )
    yield browser
    browser.close()


def pytest_generate_tests(metafunc):
    if "device_name" in metafunc.fixturenames:
        metafunc.parametrize("device_name", MOBILE_DEVICES, scope="function")


@pytest.fixture
def mobile_context(mobile_browser, device_name, playwright_instance):
    device = playwright_instance.devices[device_name]
    context = mobile_browser.new_context(
        **device,
        locale="en-US",
        timezone_id="Europe/Moscow",
    )
    yield context
    context.close()


@pytest.fixture
def mobile_page(mobile_context) -> Page:
    page = mobile_context.new_page()
    yield page
    page.close()


@pytest.fixture
def login_page(mobile_page) -> MobileLoginPage:
    return MobileLoginPage(mobile_page)


@pytest.fixture
def inventory_page(mobile_page) -> MobileInventoryPage:
    return MobileInventoryPage(mobile_page)


@pytest.fixture
def logged_in_mobile(mobile_page) -> MobileInventoryPage:
    lp = MobileLoginPage(mobile_page)
    lp.open()
    lp.login("standard_user", "secret_sauce")
    mobile_page.wait_for_url("**/inventory.html")
    return MobileInventoryPage(mobile_page)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("mobile_page")
        device = item.funcargs.get("device_name", "unknown")

        if page:
            try:
                allure.attach(
                    page.screenshot(full_page=True),
                    name=f"failure_{device.replace(' ', '_')}",
                    attachment_type=allure.attachment_type.PNG,
                )
            except Exception:
                pass
