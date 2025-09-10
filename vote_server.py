"""
Vote Server for Démocratie Permanente (demperm)

A simple voting server that enables democratic decision making through:
- Creating votes with questions and options
- Casting votes on active questions
- Retrieving voting results

This server maintains votes in memory and provides a RESTful API for voting operations.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import uuid
from typing import Dict, List, Optional

app = Flask(__name__)
CORS(app)

# In-memory storage for votes
votes: Dict[str, dict] = {}
cast_votes: Dict[str, List[dict]] = {}  # vote_id -> list of cast votes


class Vote:
    """Represents a voting question with options"""
    
    def __init__(self, question: str, options: List[str], creator: str = "anonymous"):
        self.id = str(uuid.uuid4())
        self.question = question
        self.options = options
        self.creator = creator
        self.created_at = datetime.now().isoformat()
        self.active = True
    
    def to_dict(self):
        return {
            'id': self.id,
            'question': self.question,
            'options': self.options,
            'creator': self.creator,
            'created_at': self.created_at,
            'active': self.active
        }


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Vote server is running'})


@app.route('/votes', methods=['GET'])
def get_votes():
    """Get all votes"""
    return jsonify({
        'votes': list(votes.values()),
        'count': len(votes)
    })


@app.route('/votes', methods=['POST'])
def create_vote():
    """Create a new vote"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    question = data.get('question')
    options = data.get('options')
    creator = data.get('creator', 'anonymous')
    
    if not question:
        return jsonify({'error': 'Question is required'}), 400
    
    if not options or not isinstance(options, list) or len(options) < 2:
        return jsonify({'error': 'At least 2 options are required'}), 400
    
    vote = Vote(question, options, creator)
    votes[vote.id] = vote.to_dict()
    cast_votes[vote.id] = []
    
    return jsonify({
        'message': 'Vote created successfully',
        'vote': vote.to_dict()
    }), 201


@app.route('/votes/<vote_id>', methods=['GET'])
def get_vote(vote_id: str):
    """Get a specific vote by ID"""
    if vote_id not in votes:
        return jsonify({'error': 'Vote not found'}), 404
    
    return jsonify({'vote': votes[vote_id]})


@app.route('/votes/<vote_id>/cast', methods=['POST'])
def cast_vote(vote_id: str):
    """Cast a vote for a specific option"""
    if vote_id not in votes:
        return jsonify({'error': 'Vote not found'}), 404
    
    vote = votes[vote_id]
    if not vote['active']:
        return jsonify({'error': 'Vote is no longer active'}), 400
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    option = data.get('option')
    voter_id = data.get('voter_id', 'anonymous')
    
    if option not in vote['options']:
        return jsonify({'error': 'Invalid option'}), 400
    
    # Check if voter has already voted (simple duplicate prevention)
    existing_votes = cast_votes[vote_id]
    if any(v['voter_id'] == voter_id for v in existing_votes):
        return jsonify({'error': 'Voter has already voted'}), 400
    
    cast_vote_record = {
        'voter_id': voter_id,
        'option': option,
        'timestamp': datetime.now().isoformat()
    }
    
    cast_votes[vote_id].append(cast_vote_record)
    
    return jsonify({
        'message': 'Vote cast successfully',
        'vote_id': vote_id,
        'option': option
    }), 201


@app.route('/votes/<vote_id>/results', methods=['GET'])
def get_vote_results(vote_id: str):
    """Get results for a specific vote"""
    if vote_id not in votes:
        return jsonify({'error': 'Vote not found'}), 404
    
    vote = votes[vote_id]
    votes_cast = cast_votes[vote_id]
    
    # Count votes for each option
    results = {option: 0 for option in vote['options']}
    for cast_vote in votes_cast:
        results[cast_vote['option']] += 1
    
    total_votes = len(votes_cast)
    
    return jsonify({
        'vote_id': vote_id,
        'question': vote['question'],
        'results': results,
        'total_votes': total_votes,
        'created_at': vote['created_at'],
        'active': vote['active']
    })


@app.route('/votes/<vote_id>/close', methods=['POST'])
def close_vote(vote_id: str):
    """Close a vote (make it inactive)"""
    if vote_id not in votes:
        return jsonify({'error': 'Vote not found'}), 404
    
    votes[vote_id]['active'] = False
    
    return jsonify({
        'message': 'Vote closed successfully',
        'vote_id': vote_id
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)