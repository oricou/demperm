"""Test authentication functionality."""

from fastapi.testclient import TestClient
from demperm.main import app

client = TestClient(app)


def test_register_user():
    """Test user registration."""
    response = client.post(
        "/register",
        json={
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "password123",
            "full_name": "New User"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "newuser"
    assert data["email"] == "newuser@example.com"
    assert data["full_name"] == "New User"
    assert "hashed_password" not in data


def test_register_duplicate_user():
    """Test registration with duplicate username."""
    # First registration
    client.post(
        "/register",
        json={
            "username": "duplicate",
            "email": "first@example.com",
            "password": "password123"
        }
    )
    
    # Second registration with same username
    response = client.post(
        "/register",
        json={
            "username": "duplicate",
            "email": "second@example.com",
            "password": "password123"
        }
    )
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]


def test_login():
    """Test user login."""
    # Register user first
    client.post(
        "/register",
        json={
            "username": "loginuser",
            "email": "login@example.com",
            "password": "password123"
        }
    )
    
    # Login
    response = client.post(
        "/token",
        data={
            "username": "loginuser",
            "password": "password123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials():
    """Test login with invalid credentials."""
    response = client.post(
        "/token",
        data={
            "username": "nonexistent",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]


def test_get_current_user():
    """Test getting current user information."""
    # Register and login
    client.post(
        "/register",
        json={
            "username": "currentuser",
            "email": "current@example.com",
            "password": "password123",
            "full_name": "Current User"
        }
    )
    
    token_response = client.post(
        "/token",
        data={
            "username": "currentuser",
            "password": "password123"
        }
    )
    token = token_response.json()["access_token"]
    
    # Get user info
    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "currentuser"
    assert data["email"] == "current@example.com"
    assert data["full_name"] == "Current User"


def test_get_current_user_unauthorized():
    """Test getting current user without token."""
    response = client.get("/users/me")
    assert response.status_code == 401