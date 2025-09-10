"""
Tests for the Vote Server

This module contains unit tests for the vote server functionality including:
- Creating votes
- Casting votes
- Retrieving results
- Error handling
"""

import unittest
import json
from vote_server import app


class VoteServerTestCase(unittest.TestCase):
    """Test case for the vote server"""
    
    def setUp(self):
        """Set up test client"""
        self.app = app.test_client()
        self.app.testing = True
        
        # Clear votes for each test
        from vote_server import votes, cast_votes
        votes.clear()
        cast_votes.clear()
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
    
    def test_get_empty_votes(self):
        """Test getting votes when none exist"""
        response = self.app.get('/votes')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['count'], 0)
        self.assertEqual(len(data['votes']), 0)
    
    def test_create_vote_success(self):
        """Test creating a vote successfully"""
        vote_data = {
            'question': 'What is your favorite color?',
            'options': ['Red', 'Blue', 'Green'],
            'creator': 'test_user'
        }
        response = self.app.post('/votes', 
                                data=json.dumps(vote_data),
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('vote', data)
        self.assertEqual(data['vote']['question'], vote_data['question'])
        self.assertEqual(data['vote']['options'], vote_data['options'])
        self.assertEqual(data['vote']['creator'], vote_data['creator'])
        self.assertTrue(data['vote']['active'])
    
    def test_create_vote_missing_question(self):
        """Test creating a vote without a question"""
        vote_data = {
            'options': ['Red', 'Blue', 'Green']
        }
        response = self.app.post('/votes',
                                data=json.dumps(vote_data),
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_create_vote_insufficient_options(self):
        """Test creating a vote with insufficient options"""
        vote_data = {
            'question': 'Yes or no?',
            'options': ['Yes']  # Only one option
        }
        response = self.app.post('/votes',
                                data=json.dumps(vote_data),
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_get_specific_vote(self):
        """Test getting a specific vote by ID"""
        # First create a vote
        vote_data = {
            'question': 'What is your favorite color?',
            'options': ['Red', 'Blue', 'Green']
        }
        create_response = self.app.post('/votes',
                                       data=json.dumps(vote_data),
                                       content_type='application/json')
        create_data = json.loads(create_response.data)
        vote_id = create_data['vote']['id']
        
        # Then get it
        response = self.app.get(f'/votes/{vote_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['vote']['id'], vote_id)
        self.assertEqual(data['vote']['question'], vote_data['question'])
    
    def test_get_nonexistent_vote(self):
        """Test getting a vote that doesn't exist"""
        response = self.app.get('/votes/nonexistent-id')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_cast_vote_success(self):
        """Test casting a vote successfully"""
        # First create a vote
        vote_data = {
            'question': 'What is your favorite color?',
            'options': ['Red', 'Blue', 'Green']
        }
        create_response = self.app.post('/votes',
                                       data=json.dumps(vote_data),
                                       content_type='application/json')
        create_data = json.loads(create_response.data)
        vote_id = create_data['vote']['id']
        
        # Cast a vote
        cast_data = {
            'option': 'Blue',
            'voter_id': 'voter1'
        }
        response = self.app.post(f'/votes/{vote_id}/cast',
                                data=json.dumps(cast_data),
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['option'], 'Blue')
        self.assertEqual(data['vote_id'], vote_id)
    
    def test_cast_vote_invalid_option(self):
        """Test casting a vote with an invalid option"""
        # First create a vote
        vote_data = {
            'question': 'What is your favorite color?',
            'options': ['Red', 'Blue', 'Green']
        }
        create_response = self.app.post('/votes',
                                       data=json.dumps(vote_data),
                                       content_type='application/json')
        create_data = json.loads(create_response.data)
        vote_id = create_data['vote']['id']
        
        # Cast a vote with invalid option
        cast_data = {
            'option': 'Purple',  # Not in the options
            'voter_id': 'voter1'
        }
        response = self.app.post(f'/votes/{vote_id}/cast',
                                data=json.dumps(cast_data),
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_cast_vote_duplicate_voter(self):
        """Test preventing duplicate votes from the same voter"""
        # First create a vote
        vote_data = {
            'question': 'What is your favorite color?',
            'options': ['Red', 'Blue', 'Green']
        }
        create_response = self.app.post('/votes',
                                       data=json.dumps(vote_data),
                                       content_type='application/json')
        create_data = json.loads(create_response.data)
        vote_id = create_data['vote']['id']
        
        # Cast first vote
        cast_data = {
            'option': 'Blue',
            'voter_id': 'voter1'
        }
        self.app.post(f'/votes/{vote_id}/cast',
                     data=json.dumps(cast_data),
                     content_type='application/json')
        
        # Try to cast second vote with same voter_id
        cast_data2 = {
            'option': 'Red',
            'voter_id': 'voter1'  # Same voter
        }
        response = self.app.post(f'/votes/{vote_id}/cast',
                                data=json.dumps(cast_data2),
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_get_vote_results(self):
        """Test getting vote results"""
        # First create a vote
        vote_data = {
            'question': 'What is your favorite color?',
            'options': ['Red', 'Blue', 'Green']
        }
        create_response = self.app.post('/votes',
                                       data=json.dumps(vote_data),
                                       content_type='application/json')
        create_data = json.loads(create_response.data)
        vote_id = create_data['vote']['id']
        
        # Cast some votes
        votes_to_cast = [
            {'option': 'Blue', 'voter_id': 'voter1'},
            {'option': 'Blue', 'voter_id': 'voter2'},
            {'option': 'Red', 'voter_id': 'voter3'}
        ]
        
        for vote_cast in votes_to_cast:
            self.app.post(f'/votes/{vote_id}/cast',
                         data=json.dumps(vote_cast),
                         content_type='application/json')
        
        # Get results
        response = self.app.get(f'/votes/{vote_id}/results')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        self.assertEqual(data['total_votes'], 3)
        self.assertEqual(data['results']['Blue'], 2)
        self.assertEqual(data['results']['Red'], 1)
        self.assertEqual(data['results']['Green'], 0)
    
    def test_close_vote(self):
        """Test closing a vote"""
        # First create a vote
        vote_data = {
            'question': 'What is your favorite color?',
            'options': ['Red', 'Blue', 'Green']
        }
        create_response = self.app.post('/votes',
                                       data=json.dumps(vote_data),
                                       content_type='application/json')
        create_data = json.loads(create_response.data)
        vote_id = create_data['vote']['id']
        
        # Close the vote
        response = self.app.post(f'/votes/{vote_id}/close')
        self.assertEqual(response.status_code, 200)
        
        # Verify vote is closed
        get_response = self.app.get(f'/votes/{vote_id}')
        get_data = json.loads(get_response.data)
        self.assertFalse(get_data['vote']['active'])
        
        # Try to cast vote on closed vote
        cast_data = {
            'option': 'Blue',
            'voter_id': 'voter1'
        }
        cast_response = self.app.post(f'/votes/{vote_id}/cast',
                                     data=json.dumps(cast_data),
                                     content_type='application/json')
        self.assertEqual(cast_response.status_code, 400)


if __name__ == '__main__':
    unittest.main()