# conftest.py  (root — available everywhere)
import pytest
from playwright.sync_api import Playwright, APIRequestContext
from utils.api_client import AEApiClient
from utils.data_factory import UserFactory

BASE_URL = "https://automationexercise.com"

# ── Browser & Page ────────────────────────────────────────────────────────────
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Extend default context args — add viewport, locale, etc."""
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
        "locale": "en-US",
    }

# ── API Context ───────────────────────────────────────────────────────────────
@pytest.fixture(scope="session")
def api_context(playwright: Playwright) -> APIRequestContext:
    """
    Session-scoped: one API context for the whole test run.
    Reuse this — don't create a new one per test.
    """
    context = playwright.request.new_context(base_url=BASE_URL)
    yield context
    context.dispose()

@pytest.fixture(scope="session")
def api(api_context) -> AEApiClient:
    """Thin wrapper so tests call api.get_products() not raw request methods."""
    return AEApiClient(api_context)

# ── Test User Lifecycle ───────────────────────────────────────────────────────
@pytest.fixture
def registered_user(api):
    """
    Creates a fresh user before the test, deletes them after.
    Any test that needs a real user just asks for this fixture.
    """
    user = UserFactory.build()          # generates random valid user data
    response = api.create_user(user)
    assert response.status == 200
    body = response.json()
    assert body["responseCode"] == 201, f"User creation failed: {body}"

    yield user   # the test runs here with the user data available

    # teardown — always clean up even if test fails
    api.delete_user(user["email"], user["password"])

# conftest.py — add this
@pytest.fixture
def make_user(api):
    """
    Factory fixture — call it multiple times in one test to get different users.
    All users created by this fixture are automatically deleted at end of test.
    """
    created_users = []

    def _make_user(overrides=None):
        user = UserFactory.build()
        if overrides:
            user.update(overrides)
        response = api.create_user(user)
        assert response.json()["responseCode"] == 201
        created_users.append(user)
        return user

    yield _make_user

    # teardown all created users
    for user in created_users:
        api.delete_user(user["email"], user["password"])


# Test that uses the factory:
def test_two_different_users_login(api, make_user):
    user_a = make_user()
    user_b = make_user({"name": "SpecialUser"})

    assert api.verify_login(user_a["email"], user_a["password"]).json()["responseCode"] == 200
    assert api.verify_login(user_b["email"], user_b["password"]).json()["responseCode"] == 200

# conftest.py — add this
@pytest.fixture
def authenticated_page(page, api, registered_user):
    """
    Use API to verify credentials are valid, then log in via UI.
    The page returned is already logged in.
    """
    from pages.login_page import LoginPage
    login = LoginPage(page)
    login.navigate_to_login()
    login.login(registered_user["email"], registered_user["password"])

    # Confirm UI shows logged in state before handing page to test
    page.wait_for_selector('a:has-text("Logged in as")', timeout=5000)
    yield page