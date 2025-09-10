#!/usr/bin/env python3
"""
Test script for Demperm Social Network Server
"""
import requests
import json
import sys

BASE_URL = "http://localhost:5000/api"

def test_registration():
    """Test user registration"""
    print("Testing user registration...")
    
    data = {
        "username": "alice",
        "email": "alice@example.com",
        "password": "password123",
        "bio": "Democracy enthusiast"
    }
    
    response = requests.post(f"{BASE_URL}/register", json=data)
    
    if response.status_code == 201:
        print("✓ Registration successful")
        result = response.json()
        return result.get('access_token')
    else:
        print(f"✗ Registration failed: {response.json()}")
        return None

def test_login():
    """Test user login"""
    print("Testing user login...")
    
    data = {
        "username": "alice",
        "password": "password123"
    }
    
    response = requests.post(f"{BASE_URL}/login", json=data)
    
    if response.status_code == 200:
        print("✓ Login successful")
        result = response.json()
        return result.get('access_token')
    else:
        print(f"✗ Login failed: {response.json()}")
        return None

def test_create_post(token):
    """Test creating a post"""
    print("Testing post creation...")
    
    headers = {"Authorization": f"Bearer {token}"}
    data = {"content": "Hello from the Demperm social network! #democracy"}
    
    response = requests.post(f"{BASE_URL}/posts", json=data, headers=headers)
    
    if response.status_code == 201:
        print("✓ Post creation successful")
        return response.json().get('post', {}).get('id')
    else:
        print(f"✗ Post creation failed: {response.json()}")
        return None

def test_get_posts():
    """Test getting public posts"""
    print("Testing public posts retrieval...")
    
    response = requests.get(f"{BASE_URL}/posts")
    
    if response.status_code == 200:
        result = response.json()
        posts = result.get('posts', [])
        print(f"✓ Retrieved {len(posts)} posts")
        return True
    else:
        print(f"✗ Posts retrieval failed: {response.json()}")
        return False

def test_profile(token):
    """Test getting user profile"""
    print("Testing profile retrieval...")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/profile", headers=headers)
    
    if response.status_code == 200:
        print("✓ Profile retrieval successful")
        return True
    else:
        print(f"✗ Profile retrieval failed: {response.json()}")
        return False

def main():
    """Run all tests"""
    print("Starting Demperm Social Network Server tests...\n")
    
    # Test registration
    token = test_registration()
    if not token:
        print("Cannot continue without valid token")
        return False
    
    print()
    
    # Test login (get fresh token)
    token = test_login()
    if not token:
        print("Login test failed")
        return False
    
    print()
    
    # Test profile
    test_profile(token)
    print()
    
    # Test post creation
    post_id = test_create_post(token)
    print()
    
    # Test getting posts
    test_get_posts()
    print()
    
    print("All tests completed!")
    return True

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("Error: Cannot connect to server. Make sure the server is running on localhost:5000")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)