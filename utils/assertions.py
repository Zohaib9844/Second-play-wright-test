# utils/assertions.py

def assert_api_success(response, expected_code=200):
    """Assert HTTP status and response body responseCode."""
    assert response.status == 200, f"HTTP status was {response.status}"
    body = response.json()
    assert body["responseCode"] == expected_code, (
        f"Expected responseCode {expected_code}, got {body['responseCode']}. "
        f"Message: {body.get('message', 'N/A')}"
    )
    return body  # return body for chaining

def assert_product_schema(product: dict):
    """Validate a single product object has all required fields with correct types."""
    assert isinstance(product.get("id"), int), "id must be int"
    assert isinstance(product.get("name"), str), "name must be str"
    assert isinstance(product.get("price"), str), "price must be str"
    assert "category" in product, "category must exist"