# tests/api/test_products_api.py
import pytest

pytestmark = pytest.mark.api   # tag all tests in this file

class TestProductsAPI:

    def test_get_all_products_returns_200(self, api):
        response = api.get_products()
        assert response.status == 200

    def test_products_response_has_correct_structure(self, product_list):
        assert "products" in product_list
        assert isinstance(product_list["products"], list)
        assert len(product_list["products"]) > 0

    def test_each_product_has_required_fields(self, product_list):
        required_fields = {"id", "name", "price", "brand", "category"}
        for product in product_list["products"]:
            missing = required_fields - product.keys()
            assert not missing, f"Product {product.get('id')} missing fields: {missing}"

    def test_search_product_returns_results(self, api):
        response = api.search_product("top")
        assert response.status == 200
        body = response.json()
        assert body["responseCode"] == 200
        assert len(body["products"]) > 0

    def test_search_product_missing_param_returns_400(self, api):
        """Negative test — what happens with bad input?"""
        response = api.request.post(
            "https://automationexercise.com/api/searchProduct"
            # intentionally no form data
        )
        body = response.json()
        assert body["responseCode"] == 400
        assert "missing" in body["message"].lower()

    def test_post_to_products_list_not_supported(self, api):
        """API should reject unsupported methods."""
        response = api.request.post(
            "https://automationexercise.com/api/productsList"
        )
        body = response.json()
        assert body["responseCode"] == 405