# tests/api/test_user_api.py
import pytest

pytestmark = pytest.mark.api

class TestUserCRUD:

    def test_create_user_succeeds(self, api, registered_user):
        """registered_user fixture handles create + delete — we just verify the user exists."""
        response = api.get_user_by_email(registered_user["email"])
        assert response.status == 200
        body = response.json()
        assert body["responseCode"] == 200
        assert body["user"]["email"] == registered_user["email"]

    def test_create_duplicate_user_fails(self, api, registered_user):
        """Try to register the same user twice."""
        response = api.create_user(registered_user)
        body = response.json()
        assert body["responseCode"] == 400
        assert "exists" in body["message"].lower()

    def test_update_user_name(self, api, registered_user):
        updated_data = {**registered_user, "name": "UpdatedName"}
        response = api.update_user(updated_data)
        body = response.json()
        assert body["responseCode"] == 200

        # Verify the update actually stuck
        user_response = api.get_user_by_email(registered_user["email"])
        assert user_response.json()["user"]["name"] == "UpdatedName"

    def test_get_nonexistent_user_returns_404(self, api):
        response = api.get_user_by_email("definitely_not_real_xyz@fake.com")
        body = response.json()
        assert body["responseCode"] == 404

class TestAuthAPI:

    def test_valid_login_returns_user_exists(self, api, registered_user):
        response = api.verify_login(registered_user["email"], registered_user["password"])
        body = response.json()
        assert body["responseCode"] == 200
        assert "User exists" in body["message"]

    def test_invalid_credentials_returns_404(self, api):
        response = api.verify_login("bad@email.com", "wrongpassword")
        body = response.json()
        assert body["responseCode"] == 404

    def test_login_missing_email_returns_400(self, api):
        response = api.request.post(
            "https://automationexercise.com/api/verifyLogin",
            form={"password": "somepassword"}
        )
        body = response.json()
        assert body["responseCode"] == 400

    def test_delete_method_on_login_not_supported(self, api):
        response = api.request.delete(
            "https://automationexercise.com/api/verifyLogin"
        )
        body = response.json()
        assert body["responseCode"] == 405