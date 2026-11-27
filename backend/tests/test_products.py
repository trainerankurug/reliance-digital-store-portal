from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_list_products():
    response = client.get("/api/products")
    assert response.status_code == 200
    assert len(response.json()) == 4


def test_search_products():
    response = client.get("/api/products?search=headphones")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == 102


def test_product_not_found():
    response = client.get("/api/products/999")
    assert response.status_code == 404


def test_low_stock_products():
    response = client.get("/api/products/low-stock?threshold=5")
    assert response.status_code == 200
    assert {item["id"] for item in response.json()} == {102, 103}
