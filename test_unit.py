#!/usr/bin/env python3
"""
Unit tests for Demperm Social Network Server
"""
import unittest
import tempfile
import os
from app import app, db, User, Post, Follow

class DempermTestCase(unittest.TestCase):
    
    def setUp(self):
        """Set up test database"""
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE']
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        
        with app.app_context():
            db.create_all()
    
    def tearDown(self):
        """Clean up test database"""
        with app.app_context():
            db.drop_all()
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])
    
    def test_user_model(self):
        """Test User model"""
        with app.app_context():
            user = User(username='testuser', email='test@example.com')
            user.set_password('testpass')
            db.session.add(user)
            db.session.commit()
            
            # Test password hashing
            self.assertTrue(user.check_password('testpass'))
            self.assertFalse(user.check_password('wrongpass'))
            
            # Test to_dict method
            user_dict = user.to_dict()
            self.assertEqual(user_dict['username'], 'testuser')
            self.assertEqual(user_dict['email'], 'test@example.com')
    
    def test_post_model(self):
        """Test Post model"""
        with app.app_context():
            user = User(username='testuser', email='test@example.com')
            user.set_password('testpass')
            db.session.add(user)
            db.session.commit()
            
            post = Post(content='Test post', user_id=user.id)
            db.session.add(post)
            db.session.commit()
            
            post_dict = post.to_dict()
            self.assertEqual(post_dict['content'], 'Test post')
    
    def test_follow_model(self):
        """Test Follow model"""
        with app.app_context():
            user1 = User(username='user1', email='user1@example.com')
            user1.set_password('testpass')
            user2 = User(username='user2', email='user2@example.com')
            user2.set_password('testpass')
            db.session.add(user1)
            db.session.add(user2)
            db.session.commit()
            
            follow = Follow(follower_id=user1.id, followed_id=user2.id)
            db.session.add(follow)
            db.session.commit()
            
            self.assertEqual(follow.follower_id, user1.id)
            self.assertEqual(follow.followed_id, user2.id)
    
    def test_register_endpoint(self):
        """Test user registration endpoint"""
        response = self.app.post('/api/register', 
            json={
                'username': 'newuser',
                'email': 'newuser@example.com',
                'password': 'password123'
            })
        
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('access_token', data)
        self.assertEqual(data['user']['username'], 'newuser')
    
    def test_register_validation(self):
        """Test registration validation"""
        # Missing username
        response = self.app.post('/api/register', 
            json={'email': 'test@example.com', 'password': 'pass'})
        self.assertEqual(response.status_code, 400)
        
        # Missing email
        response = self.app.post('/api/register', 
            json={'username': 'test', 'password': 'pass'})
        self.assertEqual(response.status_code, 400)
        
        # Missing password
        response = self.app.post('/api/register', 
            json={'username': 'test', 'email': 'test@example.com'})
        self.assertEqual(response.status_code, 400)
    
    def test_login_endpoint(self):
        """Test user login endpoint"""
        # First register a user
        self.app.post('/api/register', 
            json={
                'username': 'logintest',
                'email': 'logintest@example.com',
                'password': 'password123'
            })
        
        # Test successful login
        response = self.app.post('/api/login', 
            json={'username': 'logintest', 'password': 'password123'})
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('access_token', data)
        
        # Test failed login
        response = self.app.post('/api/login', 
            json={'username': 'logintest', 'password': 'wrongpass'})
        self.assertEqual(response.status_code, 401)
    
    def test_home_page(self):
        """Test home page"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Demperm Social Network Server', response.data)

if __name__ == '__main__':
    unittest.main()