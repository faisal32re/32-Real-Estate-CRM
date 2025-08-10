from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_create_and_read_client():
    response = client.post("/clients/", json={"name": "John Doe", "email": "john@example.com"})
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "john@example.com"

    response = client.get("/clients/")
    assert response.status_code == 200
    clients = response.json()
    assert len(clients) == 1
    assert clients[0]["name"] == "John Doe"


def test_create_property():
    response = client.post(
        "/properties/",
        json={"address": "123 Main St", "price": 250000.0, "sold": False, "client_id": 1},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["address"] == "123 Main St"
    response = client.get("/properties/")
    assert response.status_code == 200
    props = response.json()
    assert len(props) == 1
