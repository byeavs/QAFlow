import pytest
import allure
from playwright.sync_api import sync_playwright


def pytest_configure(config):
    config.addinivalue_line("markers", "api: API tests")
    config.addinivalue_line("markers", "ui: UI tests")
    config.addinivalue_line("markers", "e2e: E2E tests")


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        b = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"],
        )
        yield b
        b.close()


@pytest.fixture
def page(browser):
    ctx = browser.new_context(viewport={"width": 1280, "height": 720})
    pg = ctx.new_page()
    yield pg
    pg.close()
    ctx.close()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        pg = item.funcargs.get("page")
        if pg:
            try:
                allure.attach(
                    pg.screenshot(full_page=True),
                    name="screenshot_on_failure",
                    attachment_type=allure.attachment_type.PNG,
                )
            except Exception:
                pass
