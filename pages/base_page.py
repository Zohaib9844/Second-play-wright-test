# pages/base_page.py
from playwright.sync_api import Page
import os

class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.base_url = "https://automationexercise.com"

    def navigate(self, path: str = ""):
        self.page.goto(f"{self.base_url}{path}")

    def wait_for_url_contains(self, fragment: str, timeout: int = 10000):
        self.page.wait_for_url(f"**{fragment}**", timeout=timeout)

    def take_screenshot(self, name: str):
        os.makedirs("screenshots", exist_ok=True)
        self.page.screenshot(path=f"screenshots/{name}.png")