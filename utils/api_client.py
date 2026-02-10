# utils/api_client.py
from playwright.sync_api import APIRequestContext
import json

class AEApiClient:
    BASE_URL = "https://automationexercise.com/api"

    def __init__(self, request: APIRequestContext):
        self.request = request

    # ── Products ──────────────────────────────────────
    def get_products(self):
        response = self.request.get(f"{self.BASE_URL}/productsList")
        return response

    def search_product(self, keyword: str):
        response = self.request.post(
            f"{self.BASE_URL}/searchProduct",
            form={"search_product": keyword}
        )
        return response

    # ── Brands ────────────────────────────────────────
    def get_brands(self):
        return self.request.get(f"{self.BASE_URL}/brandsList")

    # ── User ──────────────────────────────────────────
    def create_user(self, user_data: dict):
        return self.request.post(
            f"{self.BASE_URL}/createAccount",
            form=user_data
        )

    def delete_user(self, email: str, password: str):
        return self.request.delete(
            f"{self.BASE_URL}/deleteAccount",
            form={"email": email, "password": password}
        )

    def update_user(self, user_data: dict):
        return self.request.put(
            f"{self.BASE_URL}/updateAccount",
            form=user_data
        )

    def get_user_by_email(self, email: str):
        return self.request.get(
            f"{self.BASE_URL}/getUserDetailByEmail",
            params={"email": email}
        )

    # ── Auth ──────────────────────────────────────────
    def verify_login(self, email: str, password: str):
        return self.request.post(
            f"{self.BASE_URL}/verifyLogin",
            form={"email": email, "password": password}
        )