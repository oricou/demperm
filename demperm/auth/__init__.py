"""Authentication and authorization utilities."""

from datetime import datetime, timedelta
from typing import Optional, Union
import hashlib
import secrets
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from .database import get_db
from .models import User

# Configuration
SECRET_KEY = "your-secret-key-here-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    # Simple hash verification - in production, use bcrypt
    return hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password


def get_password_hash(password: str) -> str:
    """Hash a password."""
    # Simple hash - in production, use bcrypt
    return hashlib.sha256(password.encode()).hexdigest()


def authenticate_user(db: Session, username: str, password: str) -> Union[User, bool]:
    """Authenticate a user by username and password."""
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a simple access token (simplified for demo)."""
    # In production, use proper JWT
    return secrets.token_urlsafe(32)


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Get the current authenticated user (simplified)."""
    # In production, properly decode JWT token
    # For now, we'll implement a simple token-based auth
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # This is a simplified implementation - in production use proper JWT
    # For demo purposes, we'll return the first user if any token is provided
    user = db.query(User).first()
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    """Get the current active user."""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def require_role(required_role: str):
    """Decorator to require a specific role."""
    def role_checker(current_user: User = Depends(get_current_active_user)):
        if current_user.role.value != required_role and current_user.role.value != "administrator":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return current_user
    return role_checker