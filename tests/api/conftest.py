# tests/api/conftest.py  (API-specific — only available to tests/api/)
import pytest

@pytest.fixture
def product_list(api):
    """Pre-fetch products once, share across tests in the module."""
    response = api.get_products()
    assert response.status == 200
    return response.json()
