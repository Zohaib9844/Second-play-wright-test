import pytest
from pages.login_page import LoginPage
from pages.products_page import ProductsPage

pytestmark = pytest.mark.e2e

class TestUserJourney:

    def test_api_register_then_ui_login(self, page, registered_user):
        """
        Pattern: API creates the user (fast) → UI logs in → assert UI confirms it.
        This is faster and more reliable than registering via UI every time.
        """
        login_page = LoginPage(page)
        login_page.navigate_to_login()
        login_page.login(registered_user["email"], registered_user["password"])

        assert login_page.is_logged_in(), "Should be logged in after valid credentials"
        assert login_page.get_logged_in_username() == registered_user["name"]

    def test_wrong_password_shows_error(self, page, registered_user):
        """
        User exists (created via API) but wrong password used in UI.
        Verifies the error message appears correctly.
        """
        login_page = LoginPage(page)
        login_page.navigate_to_login()
        login_page.login(registered_user["email"], "WrongPassword999!")

        assert not login_page.is_logged_in(), "Should NOT be logged in with wrong password"
        assert login_page.get_error_message() is not None

    def test_api_user_verified_then_ui_login(self, page, api, registered_user):
        """
        Step 1 — confirm user is valid via API first.
        Step 2 — then log in via UI.
        Useful pattern when you want to rule out API issues before blaming UI.
        """
        # Verify via API first
        verify_response = api.verify_login(
            registered_user["email"], registered_user["password"]
        )
        body = verify_response.json()
        assert body["responseCode"] == 200, f"API login check failed: {body}"

        # Now try the same credentials in the UI
        login_page = LoginPage(page)
        login_page.navigate_to_login()
        login_page.login(registered_user["email"], registered_user["password"])

        assert login_page.is_logged_in()

    def test_api_search_results_match_ui(self, page, api):
        """
        Cross-verify: search the same keyword via API and via UI.
        Both should return results. Great for catching data/sync bugs.
        """
        keyword = "top"

        # API side
        api_response = api.search_product(keyword)
        api_body = api_response.json()
        assert api_body["responseCode"] == 200
        api_count = len(api_body["products"])
        assert api_count > 0, "API returned no products for keyword 'top'"

        # UI side
        products_page = ProductsPage(page)
        products_page.navigate_to_products()
        products_page.search(keyword)

        ui_names = products_page.get_product_names()
        assert len(ui_names) > 0, "UI returned no products for keyword 'top'"

        # Both found results — counts don't have to match exactly
        # (UI may paginate) but at minimum both must be non-empty
        print(f"\nAPI found {api_count} products | UI found {len(ui_names)} products")