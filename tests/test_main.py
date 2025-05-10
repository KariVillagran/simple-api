import pytest
from fastapi.testclient import TestClient
from app.main import app  # Importa directamente la instancia de la app
from app.database import Base, engine  # Base y engine están en database.py

client = TestClient(app)

# Setup y teardown para cada test
@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_item():
    response = client.post("/items/", json={"name": "Item1", "description": "Test item"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Item1"
    assert data["description"] == "Test item"
    assert "id" in data

def test_read_items_empty():
    response = client.get("/items/")
    assert response.status_code == 200
    assert response.json() == []

def test_read_items_after_insert():
    client.post("/items/", json={"name": "Item1", "description": "Item 1"})
    client.post("/items/", json={"name": "Item2", "description": "Item 2"})

    response = client.get("/items/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Item1"
    assert data[1]["name"] == "Item2"

