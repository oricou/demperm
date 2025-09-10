#!/usr/bin/env python3
"""
DemPerm - Démocratie Permanente Web Client
A simple web interface for democratic processes
"""

from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')

# In-memory storage for demo purposes
votes = {}
proposals = []

@app.route('/')
def index():
    """Main page showing current proposals and voting status"""
    return render_template('index.html', proposals=proposals, votes=votes)

@app.route('/vote/<int:proposal_id>', methods=['POST'])
def vote(proposal_id):
    """Cast a vote on a proposal"""
    if proposal_id >= len(proposals):
        flash('Proposal not found', 'error')
        return redirect(url_for('index'))
    
    vote_choice = request.form.get('vote')
    if vote_choice in ['yes', 'no', 'abstain']:
        if proposal_id not in votes:
            votes[proposal_id] = {'yes': 0, 'no': 0, 'abstain': 0}
        votes[proposal_id][vote_choice] += 1
        flash('Vote cast successfully!', 'success')
    else:
        flash('Invalid vote choice', 'error')
    
    return redirect(url_for('index'))

@app.route('/propose', methods=['GET', 'POST'])
def propose():
    """Submit a new proposal"""
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        
        if title and description:
            proposals.append({
                'title': title,
                'description': description,
                'id': len(proposals)
            })
            flash('Proposal submitted successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Title and description are required', 'error')
    
    return render_template('propose.html')

@app.route('/about')
def about():
    """About page explaining the democratic process"""
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)