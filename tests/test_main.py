from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app, get_db
from app import models
from app.models import Base

# ---------- TEST DATABASE SETUP ----------
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Recreate tables before tests
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

# Dependency override
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# ---------- TESTS BEGIN HERE ----------

def test_get_products_empty():
    response = client.get("/products")
    assert response.status_code == 200
    assert response.json() == []

def test_add_products_and_place_order():
    db = TestingSessionLocal()
    # Insert products
    laptop = models.Product(name="Laptop", price=1000.0, stock=5)
    mouse = models.Product(name="Mouse", price=20.0, stock=50)
    db.add_all([laptop, mouse])
    db.commit()

    # Fetch inserted product IDs
    db.refresh(laptop)
    db.refresh(mouse)

    # Verify GET /products
    response = client.get("/products")
    assert response.status_code == 200
    products = response.json()
    assert len(products) == 2
    assert any(p["name"] == "Laptop" for p in products)
    assert any(p["name"] == "Mouse" for p in products)

    # Place order
    payload = {
        "items": [
            {"product_id": laptop.id, "quantity": 1},
            {"product_id": mouse.id, "quantity": 2}
        ]
    }
    response = client.post("/orders", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "order_id" in data
    assert data["total"] > 0

def test_insufficient_stock():
    db = TestingSessionLocal()
    monitor = models.Product(name="Monitor", price=200.0, stock=1)
    db.add(monitor)
    db.commit()
    db.refresh(monitor)

    payload = {
        "items": [
            {"product_id": monitor.id, "quantity": 5}
        ]
    }
    response = client.post("/orders", json=payload)
    assert response.status_code == 400
    assert "Insufficient stock" in response.json()["detail"]
