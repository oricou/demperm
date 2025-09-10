from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///demperm.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-change-in-production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

# Initialize extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    bio = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    posts = db.relationship('Post', backref='author', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'bio': self.bio,
            'created_at': self.created_at.isoformat(),
            'post_count': len(self.posts)
        }

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'created_at': self.created_at.isoformat(),
            'author': {
                'id': self.author.id,
                'username': self.author.username
            }
        }

class Follow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Ensure unique follower-followed pairs
    __table_args__ = (db.UniqueConstraint('follower_id', 'followed_id'),)

# API Routes

@app.route('/api/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Username, email, and password are required'}), 400
    
    # Check if user already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    # Create new user
    user = User(
        username=data['username'],
        email=data['email'],
        bio=data.get('bio', '')
    )
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    # Create access token
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        'message': 'User registered successfully',
        'user': user.to_dict(),
        'access_token': access_token
    }), 201

@app.route('/api/login', methods=['POST'])
def login():
    """Login user"""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password are required'}), 400
    
    user = User.query.filter_by(username=data['username']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid username or password'}), 401
    
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        'message': 'Login successful',
        'user': user.to_dict(),
        'access_token': access_token
    })

@app.route('/api/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get current user's profile"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user.to_dict())

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get user by ID"""
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user.to_dict())

@app.route('/api/posts', methods=['POST'])
@jwt_required()
def create_post():
    """Create a new post"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data or not data.get('content'):
        return jsonify({'error': 'Content is required'}), 400
    
    post = Post(
        content=data['content'],
        user_id=user_id
    )
    
    db.session.add(post)
    db.session.commit()
    
    return jsonify({
        'message': 'Post created successfully',
        'post': post.to_dict()
    }), 201

@app.route('/api/posts', methods=['GET'])
def get_posts():
    """Get all posts (public timeline)"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    posts = Post.query.order_by(Post.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'posts': [post.to_dict() for post in posts.items],
        'pagination': {
            'page': posts.page,
            'pages': posts.pages,
            'per_page': posts.per_page,
            'total': posts.total
        }
    })

@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    """Delete a post (only by author)"""
    user_id = get_jwt_identity()
    post = Post.query.get(post_id)
    
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    
    if post.user_id != user_id:
        return jsonify({'error': 'You can only delete your own posts'}), 403
    
    db.session.delete(post)
    db.session.commit()
    
    return jsonify({'message': 'Post deleted successfully'})

@app.route('/api/follow/<int:user_id>', methods=['POST'])
@jwt_required()
def follow_user(user_id):
    """Follow a user"""
    follower_id = get_jwt_identity()
    
    if follower_id == user_id:
        return jsonify({'error': 'You cannot follow yourself'}), 400
    
    # Check if user exists
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Check if already following
    existing_follow = Follow.query.filter_by(
        follower_id=follower_id,
        followed_id=user_id
    ).first()
    
    if existing_follow:
        return jsonify({'error': 'Already following this user'}), 400
    
    # Create follow relationship
    follow = Follow(follower_id=follower_id, followed_id=user_id)
    db.session.add(follow)
    db.session.commit()
    
    return jsonify({'message': f'Now following {user.username}'})

@app.route('/api/unfollow/<int:user_id>', methods=['DELETE'])
@jwt_required()
def unfollow_user(user_id):
    """Unfollow a user"""
    follower_id = get_jwt_identity()
    
    follow = Follow.query.filter_by(
        follower_id=follower_id,
        followed_id=user_id
    ).first()
    
    if not follow:
        return jsonify({'error': 'Not following this user'}), 400
    
    db.session.delete(follow)
    db.session.commit()
    
    return jsonify({'message': 'Unfollowed successfully'})

@app.route('/api/feed', methods=['GET'])
@jwt_required()
def get_feed():
    """Get posts from followed users"""
    user_id = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Get IDs of users being followed
    followed_users = db.session.query(Follow.followed_id).filter_by(follower_id=user_id)
    
    # Get posts from followed users (including own posts)
    posts = Post.query.filter(
        db.or_(
            Post.user_id.in_(followed_users),
            Post.user_id == user_id
        )
    ).order_by(Post.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'posts': [post.to_dict() for post in posts.items],
        'pagination': {
            'page': posts.page,
            'pages': posts.pages,
            'per_page': posts.per_page,
            'total': posts.total
        }
    })

@app.route('/api/users/<int:user_id>/followers', methods=['GET'])
def get_followers(user_id):
    """Get list of user's followers"""
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    followers = db.session.query(User).join(
        Follow, Follow.follower_id == User.id
    ).filter(Follow.followed_id == user_id).all()
    
    return jsonify({
        'followers': [user.to_dict() for user in followers]
    })

@app.route('/api/users/<int:user_id>/following', methods=['GET'])
def get_following(user_id):
    """Get list of users that this user follows"""
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    following = db.session.query(User).join(
        Follow, Follow.followed_id == User.id
    ).filter(Follow.follower_id == user_id).all()
    
    return jsonify({
        'following': [user.to_dict() for user in following]
    })

# Basic web interface for testing
@app.route('/')
def index():
    """Basic landing page"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Demperm - Social Network</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .container { max-width: 800px; margin: 0 auto; }
            .endpoint { background: #f5f5f5; padding: 10px; margin: 10px 0; border-radius: 5px; }
            .method { font-weight: bold; color: #2196F3; }
            .method.POST { color: #4CAF50; }
            .method.DELETE { color: #f44336; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Demperm Social Network Server</h1>
            <p>A simple social network server for permanent democracy discussions.</p>
            
            <h2>API Endpoints</h2>
            
            <div class="endpoint">
                <span class="method POST">POST</span> /api/register - Register a new user
            </div>
            
            <div class="endpoint">
                <span class="method POST">POST</span> /api/login - Login user
            </div>
            
            <div class="endpoint">
                <span class="method">GET</span> /api/profile - Get current user profile (requires auth)
            </div>
            
            <div class="endpoint">
                <span class="method">GET</span> /api/users/&lt;id&gt; - Get user by ID
            </div>
            
            <div class="endpoint">
                <span class="method POST">POST</span> /api/posts - Create a new post (requires auth)
            </div>
            
            <div class="endpoint">
                <span class="method">GET</span> /api/posts - Get all posts (public timeline)
            </div>
            
            <div class="endpoint">
                <span class="method DELETE">DELETE</span> /api/posts/&lt;id&gt; - Delete post (requires auth)
            </div>
            
            <div class="endpoint">
                <span class="method POST">POST</span> /api/follow/&lt;user_id&gt; - Follow user (requires auth)
            </div>
            
            <div class="endpoint">
                <span class="method DELETE">DELETE</span> /api/unfollow/&lt;user_id&gt; - Unfollow user (requires auth)
            </div>
            
            <div class="endpoint">
                <span class="method">GET</span> /api/feed - Get personalized feed (requires auth)
            </div>
            
            <div class="endpoint">
                <span class="method">GET</span> /api/users/&lt;id&gt;/followers - Get user's followers
            </div>
            
            <div class="endpoint">
                <span class="method">GET</span> /api/users/&lt;id&gt;/following - Get who user follows
            </div>
            
            <h2>Usage Example</h2>
            <p>1. Register: <code>curl -X POST http://localhost:5000/api/register -H "Content-Type: application/json" -d '{"username":"alice","email":"alice@example.com","password":"password123"}'</code></p>
            <p>2. Login: <code>curl -X POST http://localhost:5000/api/login -H "Content-Type: application/json" -d '{"username":"alice","password":"password123"}'</code></p>
            <p>3. Create post: <code>curl -X POST http://localhost:5000/api/posts -H "Content-Type: application/json" -H "Authorization: Bearer YOUR_TOKEN" -d '{"content":"Hello, democracy!"}'</code></p>
        </div>
    </body>
    </html>
    '''

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# Initialize database
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)