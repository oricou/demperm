# Demperm - Social Network Server
Démocratie permanente - A social network server for democratic participation and discussion.

## Features

This social network server provides the following core functionality:

- **User Management**: Registration, authentication, and profiles
- **Content Creation**: Users can create and share posts
- **Social Features**: Follow/unfollow other users
- **Personalized Feed**: View posts from followed users
- **Public Timeline**: Browse all posts in the network
- **REST API**: Complete API for all functionality

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd demperm
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run the server:
```bash
python app.py
```

The server will start on `http://localhost:5000`

## API Documentation

### Authentication

Most endpoints require authentication using JWT tokens. Include the token in the Authorization header:
```
Authorization: Bearer <your-token>
```

### Endpoints

#### User Management
- `POST /api/register` - Register a new user
- `POST /api/login` - Login and get access token
- `GET /api/profile` - Get current user profile (requires auth)
- `GET /api/users/<id>` - Get user by ID

#### Posts
- `POST /api/posts` - Create a new post (requires auth)
- `GET /api/posts` - Get all posts (public timeline)
- `DELETE /api/posts/<id>` - Delete post (requires auth, own posts only)
- `GET /api/feed` - Get personalized feed (requires auth)

#### Social Features
- `POST /api/follow/<user_id>` - Follow a user (requires auth)
- `DELETE /api/unfollow/<user_id>` - Unfollow a user (requires auth)
- `GET /api/users/<id>/followers` - Get user's followers
- `GET /api/users/<id>/following` - Get who user follows

## Usage Examples

### Register a new user:
```bash
curl -X POST http://localhost:5000/api/register \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","email":"alice@example.com","password":"password123"}'
```

### Login:
```bash
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"password123"}'
```

### Create a post:
```bash
curl -X POST http://localhost:5000/api/posts \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"content":"Hello, democracy!"}'
```

### Follow a user:
```bash
curl -X POST http://localhost:5000/api/follow/2 \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Testing

Run the test script to verify the API functionality:
```bash
python test_api.py
```

Make sure the server is running before executing the tests.

## Technology Stack

- **Backend**: Flask (Python web framework)
- **Database**: SQLite (with SQLAlchemy ORM)
- **Authentication**: JWT tokens
- **Password Security**: Bcrypt hashing

## Database Schema

### Users Table
- `id`: Primary key
- `username`: Unique username
- `email`: Unique email address
- `password_hash`: Bcrypt hashed password
- `bio`: User biography
- `created_at`: Registration timestamp

### Posts Table
- `id`: Primary key
- `content`: Post content
- `user_id`: Foreign key to users table
- `created_at`: Post creation timestamp

### Follow Table
- `id`: Primary key
- `follower_id`: Foreign key to users table (who follows)
- `followed_id`: Foreign key to users table (who is being followed)
- `created_at`: Follow relationship timestamp

## License

This project is licensed under the GNU General Public License v3.0 - see the LICENSE file for details.
