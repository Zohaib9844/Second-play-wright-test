# pages/signup_page.py
from pages.base_page import BasePage

class SignupPage(BasePage):
    NAME_INPUT = 'input[data-qa="signup-name"]'
    EMAIL_INPUT = 'input[data-qa="signup-email"]'
    SIGNUP_BUTTON = 'button[data-qa="signup-button"]'
    # Account creation form fields
    PASSWORD_INPUT = 'input[data-qa="password"]'
    FIRST_NAME = 'input[data-qa="first_name"]'
    LAST_NAME = 'input[data-qa="last_name"]'
    ADDRESS = 'input[data-qa="address"]'
    STATE = 'input[data-qa="state"]'
    CITY = 'input[data-qa="city"]'
    ZIPCODE = 'input[data-qa="zipcode"]'
    MOBILE = 'input[data-qa="mobile_number"]'
    CREATE_ACCOUNT_BUTTON = 'button[data-qa="create-account"]'
    ACCOUNT_CREATED_MSG = 'h2[data-qa="account-created"]'

    def navigate_to_signup(self):
        self.navigate("/login")

    def fill_signup_name_email(self, name: str, email: str):
        self.page.fill(self.NAME_INPUT, name)
        self.page.fill(self.EMAIL_INPUT, email)
        self.page.click(self.SIGNUP_BUTTON)

    def fill_account_details(self, user_data: dict):
        self.page.fill(self.PASSWORD_INPUT, user_data["password"])
        self.page.fill(self.FIRST_NAME, user_data["firstname"])
        self.page.fill(self.LAST_NAME, user_data["lastname"])
        self.page.fill(self.ADDRESS, user_data["address1"])
        self.page.fill(self.STATE, user_data["state"])
        self.page.fill(self.CITY, user_data["city"])
        self.page.fill(self.ZIPCODE, user_data["zipcode"])
        self.page.fill(self.MOBILE, user_data["mobile_number"])
        self.page.click(self.CREATE_ACCOUNT_BUTTON)

    def is_account_created(self) -> bool:
        return self.page.is_visible(self.ACCOUNT_CREATED_MSG)