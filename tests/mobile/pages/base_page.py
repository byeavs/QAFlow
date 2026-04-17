from playwright.sync_api import Page


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str):
        self.page.goto(url, wait_until="domcontentloaded")

    def get_title(self) -> str:
        return self.page.title()

    def wait_for_url(self, pattern: str):
        self.page.wait_for_url(pattern)

    def is_mobile_viewport(self) -> bool:
        width = self.page.viewport_size["width"]
        return width <= 768

    def get_viewport(self) -> dict:
        return self.page.viewport_size
