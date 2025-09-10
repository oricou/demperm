"""Test proposal functionality."""

from fastapi.testclient import TestClient
from demperm.main import app

client = TestClient(app)


def test_create_proposal():
    """Test creating a new proposal."""
    # Register and login first
    client.post(
        "/register",
        json={
            "username": "proposer",
            "email": "proposer@example.com",
            "password": "password123",
            "full_name": "Proposer User"
        }
    )
    
    token_response = client.post(
        "/token",
        data={
            "username": "proposer",
            "password": "password123"
        }
    )
    token = token_response.json()["access_token"]
    
    # Create proposal
    response = client.post(
        "/proposals",
        json={
            "title": "Test Proposal",
            "description": "This is a test proposal for the democracy platform",
            "content": "Detailed content about the proposal",
            "vote_type": "yes_no"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Proposal"
    assert data["description"] == "This is a test proposal for the democracy platform"
    assert data["status"] == "draft"
    assert data["vote_type"] == "yes_no"


def test_list_proposals():
    """Test listing proposals."""
    response = client.get("/proposals")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_proposal():
    """Test getting a specific proposal."""
    # Create a proposal first
    client.post(
        "/register",
        json={
            "username": "proposer2",
            "email": "proposer2@example.com",
            "password": "password123"
        }
    )
    
    token_response = client.post(
        "/token",
        data={
            "username": "proposer2",
            "password": "password123"
        }
    )
    token = token_response.json()["access_token"]
    
    create_response = client.post(
        "/proposals",
        json={
            "title": "Specific Proposal",
            "description": "Proposal for specific testing",
            "vote_type": "yes_no"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    proposal_id = create_response.json()["id"]
    
    # Get the proposal
    response = client.get(f"/proposals/{proposal_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == proposal_id
    assert data["title"] == "Specific Proposal"


def test_get_nonexistent_proposal():
    """Test getting a non-existent proposal."""
    response = client.get("/proposals/99999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_create_proposal_unauthorized():
    """Test creating a proposal without authentication."""
    response = client.post(
        "/proposals",
        json={
            "title": "Unauthorized Proposal",
            "description": "This should fail",
            "vote_type": "yes_no"
        }
    )
    assert response.status_code == 401