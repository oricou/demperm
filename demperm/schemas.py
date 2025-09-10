"""Pydantic schemas for request/response validation."""

from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    """User roles."""
    CITIZEN = "citizen"
    MODERATOR = "moderator"
    ADMINISTRATOR = "administrator"


class VoteType(str, Enum):
    """Vote types."""
    YES_NO = "yes_no"
    APPROVAL = "approval"
    RANKING = "ranking"
    SCORE = "score"


class ProposalStatus(str, Enum):
    """Proposal status."""
    DRAFT = "draft"
    DISCUSSION = "discussion"
    VOTING = "voting"
    CLOSED = "closed"
    IMPLEMENTED = "implemented"
    REJECTED = "rejected"


# User schemas
class UserBase(BaseModel):
    """Base user schema."""
    username: str
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    """Schema for user creation."""
    password: str

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v


class UserUpdate(BaseModel):
    """Schema for user updates."""
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None


class User(UserBase):
    """User response schema."""
    id: int
    role: UserRole
    is_active: bool
    is_verified: bool
    created_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True


# Category schemas
class CategoryBase(BaseModel):
    """Base category schema."""
    name: str
    description: Optional[str] = None
    color: str = "#007bff"


class CategoryCreate(CategoryBase):
    """Schema for category creation."""
    pass


class Category(CategoryBase):
    """Category response schema."""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Proposal schemas
class ProposalBase(BaseModel):
    """Base proposal schema."""
    title: str
    description: str
    content: Optional[str] = None
    vote_type: VoteType = VoteType.YES_NO
    category_id: Optional[int] = None


class ProposalCreate(ProposalBase):
    """Schema for proposal creation."""
    pass


class ProposalUpdate(BaseModel):
    """Schema for proposal updates."""
    title: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
    status: Optional[ProposalStatus] = None
    discussion_start: Optional[datetime] = None
    discussion_end: Optional[datetime] = None
    voting_start: Optional[datetime] = None
    voting_end: Optional[datetime] = None


class Proposal(ProposalBase):
    """Proposal response schema."""
    id: int
    status: ProposalStatus
    created_at: datetime
    discussion_start: Optional[datetime] = None
    discussion_end: Optional[datetime] = None
    voting_start: Optional[datetime] = None
    voting_end: Optional[datetime] = None
    author_id: int
    author: User
    category: Optional[Category] = None

    class Config:
        from_attributes = True


# Vote schemas
class VoteBase(BaseModel):
    """Base vote schema."""
    value: str
    comment: Optional[str] = None


class VoteCreate(VoteBase):
    """Schema for vote creation."""
    proposal_id: int


class Vote(VoteBase):
    """Vote response schema."""
    id: int
    created_at: datetime
    user_id: int
    proposal_id: int
    user: User

    class Config:
        from_attributes = True


# Comment schemas
class CommentBase(BaseModel):
    """Base comment schema."""
    content: str


class CommentCreate(CommentBase):
    """Schema for comment creation."""
    proposal_id: int
    parent_id: Optional[int] = None


class CommentUpdate(BaseModel):
    """Schema for comment updates."""
    content: str


class Comment(CommentBase):
    """Comment response schema."""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    is_deleted: bool
    author_id: int
    proposal_id: int
    parent_id: Optional[int] = None
    author: User

    class Config:
        from_attributes = True


# Vote results schemas
class VoteResultBase(BaseModel):
    """Base vote result schema."""
    total_votes: int
    yes_votes: int = 0
    no_votes: int = 0
    approval_votes: int = 0
    average_score: Optional[float] = None
    winner: Optional[str] = None
    result_data: Optional[str] = None


class VoteResult(VoteResultBase):
    """Vote result response schema."""
    id: int
    proposal_id: int
    calculated_at: datetime

    class Config:
        from_attributes = True


# Authentication schemas
class Token(BaseModel):
    """Token response schema."""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Token data schema."""
    username: Optional[str] = None


# Dashboard schemas
class DashboardStats(BaseModel):
    """Dashboard statistics schema."""
    total_users: int
    active_proposals: int
    total_votes: int
    recent_proposals: List[Proposal]