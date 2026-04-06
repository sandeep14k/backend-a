import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from database import Base, get_db

# 1. Setup a temporary, in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the tables in the test database
Base.metadata.create_all(bind=engine)

# 2. Override the get_db dependency to use the test database
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# 3. Initialize the TestClient
client = TestClient(app)

# ==========================================
# ACTUAL AUTOMATED TESTS
# ==========================================

def test_create_admin_user():
    """Test that we can successfully create a new admin user."""
    response = client.post(
        "/users/",
        json={"username": "test_admin", "role": "admin"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "test_admin"
    assert data["role"] == "admin"
    assert "id" in data

def test_duplicate_user_handling():
    """Test our enterprise error handling for duplicate usernames."""
    # First, create a user
    client.post("/users/", json={"username": "unique_guy", "role": "viewer"})
    
    # Second, try to create the EXACT same user again
    response = client.post("/users/", json={"username": "unique_guy", "role": "viewer"})
    
    # We expect our custom 400 error, NOT a 500 server crash!
    assert response.status_code == 400
    assert response.json()["detail"] == "That username is already taken. Please choose another."

def test_rbac_security_blocks_viewer():
    """Test that a 'viewer' cannot create a financial record (Role-Based Access Control)."""
    # 1. Create a viewer user
    user_response = client.post("/users/", json={"username": "sad_viewer", "role": "viewer"})
    viewer_id = user_response.json()["id"]
    
    # 2. Try to create a record using the viewer's ID in the headers
    record_response = client.post(
        "/records/",
        headers={"user-id": str(viewer_id)},
        json={
            "amount": 100,
            "type": "expense",
            "category": "Snacks",
            "notes": "Should be blocked"
        }
    )
    
    # 3. Verify they are blocked by the auth dependency
    assert record_response.status_code == 403
    assert "Admin privileges required" in record_response.json()["detail"]