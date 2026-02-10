# pages/login_page.py
from pages.base_page import BasePage

class LoginPage(BasePage):
    # Selectors — ONLY defined here, never in tests
    EMAIL_INPUT = 'input[data-qa="login-email"]'
    PASSWORD_INPUT = 'input[data-qa="login-password"]'
    LOGIN_BUTTON = 'button[data-qa="login-button"]'
    ERROR_MESSAGE = 'p:has-text("Your email or password is incorrect!")'
    LOGGED_IN_INDICATOR = 'a:has-text("Logged in as")'

    def navigate_to_login(self):
        self.navigate("/login")
        self.page.wait_for_load_state("networkidle")  # wait for ads to load before we try anything

    def login(self, email: str, password: str):
        # Wait for page to fully settle before interacting
        self.page.wait_for_load_state("networkidle")
        
        # Dismiss any ad overlay if present
        try:
            ad = self.page.locator("div[id*='ad'], iframe[id*='google_ads'], .adsbygoogle").first
            if ad.is_visible(timeout=2000):
                self.page.evaluate("document.querySelectorAll('iframe[id*=\"google\"], .adsbygoogle').forEach(e => e.remove())")
        except:
            pass  # No ad, carry on
        
        self.page.fill(self.EMAIL_INPUT, email)
        self.page.fill(self.PASSWORD_INPUT, password)
        
        # Use force=True to click through any remaining overlay
        self.page.click(self.LOGIN_BUTTON, force=True)
        
        # Give the page time to redirect after login
        self.page.wait_for_load_state("domcontentloaded")
        
    def get_error_message(self) -> str:
        return self.page.text_content(self.ERROR_MESSAGE)

    def is_logged_in(self) -> bool:
        return self.page.is_visible(self.LOGGED_IN_INDICATOR)

    def get_logged_in_username(self) -> str:
        """Extract 'John' from 'Logged in as John'"""
        text = self.page.text_content(self.LOGGED_IN_INDICATOR)
        return text.replace("Logged in as", "").strip()