# demperm - Vote Server
Démocratie permanente (Permanent Democracy) - A simple voting server for democratic decision making.

## Overview

This vote server enables democratic participation through a simple REST API that allows:
- Creating voting questions with multiple options
- Casting votes on active questions  
- Retrieving voting results in real-time
- Managing vote lifecycle (opening/closing votes)

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
python vote_server.py
```

The server will start on `http://localhost:5000`

## API Endpoints

### Health Check
- **GET** `/health` - Check if the server is running

### Vote Management
- **GET** `/votes` - Get all votes
- **POST** `/votes` - Create a new vote
- **GET** `/votes/{vote_id}` - Get a specific vote
- **POST** `/votes/{vote_id}/close` - Close a vote (make it inactive)

### Voting
- **POST** `/votes/{vote_id}/cast` - Cast a vote
- **GET** `/votes/{vote_id}/results` - Get voting results

## Usage Examples

### Create a Vote
```bash
curl -X POST http://localhost:5000/votes \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What should we have for lunch?",
    "options": ["Pizza", "Burgers", "Salad"],
    "creator": "alice"
  }'
```

### Cast a Vote
```bash
curl -X POST http://localhost:5000/votes/{vote_id}/cast \
  -H "Content-Type: application/json" \
  -d '{
    "option": "Pizza",
    "voter_id": "bob"
  }'
```

### Get Results
```bash
curl http://localhost:5000/votes/{vote_id}/results
```

## Testing

Run the test suite:
```bash
python -m pytest test_vote_server.py -v
```

Or with unittest:
```bash
python test_vote_server.py
```

## Features

- **Simple REST API**: Easy to integrate with web applications
- **In-memory storage**: Fast and simple (for development/demo purposes)
- **Duplicate vote prevention**: Each voter can only vote once per question
- **Real-time results**: Get current voting results at any time
- **Vote lifecycle management**: Create, activate, and close votes
- **CORS enabled**: Can be used from web browsers

## Data Models

### Vote
```json
{
  "id": "uuid",
  "question": "string",
  "options": ["string"],
  "creator": "string", 
  "created_at": "ISO datetime",
  "active": boolean
}
```

### Vote Results
```json
{
  "vote_id": "uuid",
  "question": "string", 
  "results": {"option": count},
  "total_votes": number,
  "created_at": "ISO datetime",
  "active": boolean
}
```
