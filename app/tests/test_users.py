# app/tests/test_users.py
import sys
import os

# Add the app/src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_create_user():
    """Test creating a new user."""
    response = client.post(
        "/api/v1/users/",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "full_name": "Test User",
            "password": "testpass"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "id" in data

def test_create_duplicate_user():
    """Test creating a user with an existing email."""
    client.post(
        "/api/v1/users/",
        json={
            "username": "testuser2",
            "email": "duplicate@example.com",
            "full_name": "Test User 2",
            "password": "testpass"
        }
    )
    # Try to create another user with the same email
    response = client.post(
        "/api/v1/users/",
        json={
            "username": "testuser3",
            "email": "duplicate@example.com",
            "full_name": "Test User 3",
            "password": "testpass"
        }
    )
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]

def test_get_users():
    """Test retrieving a list of users."""
    response = client.get("/api/v1/users/?skip=0&limit=10")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_nonexistent_user():
    """Test retrieving a user that doesn't exist."""
    response = client.get("/api/v1/users/9999")
    assert response.status_code == 404

def test_root_endpoint():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"