"""Database models for the democracy platform."""

from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()


class UserRole(enum.Enum):
    """User roles in the democracy platform."""
    CITIZEN = "citizen"
    MODERATOR = "moderator"
    ADMINISTRATOR = "administrator"


class VoteType(enum.Enum):
    """Different types of voting mechanisms."""
    YES_NO = "yes_no"
    APPROVAL = "approval"
    RANKING = "ranking"
    SCORE = "score"


class ProposalStatus(enum.Enum):
    """Status of a proposal in the democratic process."""
    DRAFT = "draft"
    DISCUSSION = "discussion"
    VOTING = "voting"
    CLOSED = "closed"
    IMPLEMENTED = "implemented"
    REJECTED = "rejected"


class User(Base):
    """User model for citizens and administrators."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(128), nullable=False)
    full_name = Column(String(100))
    role = Column(SQLEnum(UserRole), default=UserRole.CITIZEN, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_login = Column(DateTime)

    # Relationships
    proposals = relationship("Proposal", back_populates="author")
    votes = relationship("Vote", back_populates="user")
    comments = relationship("Comment", back_populates="author")


class Category(Base):
    """Categories for organizing proposals."""
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    color = Column(String(7), default="#007bff")  # Hex color code
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    proposals = relationship("Proposal", back_populates="category")


class Proposal(Base):
    """Proposals for democratic consideration."""
    __tablename__ = "proposals"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    content = Column(Text)  # Detailed content/reasoning
    status = Column(SQLEnum(ProposalStatus), default=ProposalStatus.DRAFT, nullable=False)
    vote_type = Column(SQLEnum(VoteType), default=VoteType.YES_NO, nullable=False)
    
    # Timing
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    discussion_start = Column(DateTime)
    discussion_end = Column(DateTime)
    voting_start = Column(DateTime)
    voting_end = Column(DateTime)
    
    # Relationships
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"))
    
    author = relationship("User", back_populates="proposals")
    category = relationship("Category", back_populates="proposals")
    votes = relationship("Vote", back_populates="proposal")
    comments = relationship("Comment", back_populates="proposal")


class Vote(Base):
    """Votes cast by users on proposals."""
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, index=True)
    value = Column(String(50), nullable=False)  # "yes", "no", "approve", score, or ranking
    comment = Column(Text)  # Optional comment with the vote
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    proposal_id = Column(Integer, ForeignKey("proposals.id"), nullable=False)
    
    user = relationship("User", back_populates="votes")
    proposal = relationship("Proposal", back_populates="votes")


class Comment(Base):
    """Comments on proposals for discussion."""
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    is_deleted = Column(Boolean, default=False, nullable=False)
    
    # Relationships
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    proposal_id = Column(Integer, ForeignKey("proposals.id"), nullable=False)
    parent_id = Column(Integer, ForeignKey("comments.id"))  # For threaded comments
    
    author = relationship("User", back_populates="comments")
    proposal = relationship("Proposal", back_populates="comments")
    parent = relationship("Comment", remote_side="Comment.id")


class VoteResult(Base):
    """Aggregated results for proposals."""
    __tablename__ = "vote_results"

    id = Column(Integer, primary_key=True, index=True)
    proposal_id = Column(Integer, ForeignKey("proposals.id"), unique=True, nullable=False)
    total_votes = Column(Integer, default=0, nullable=False)
    yes_votes = Column(Integer, default=0, nullable=False)
    no_votes = Column(Integer, default=0, nullable=False)
    approval_votes = Column(Integer, default=0, nullable=False)
    average_score = Column(Integer)  # For score-based voting
    winner = Column(String(100))  # For ranking-based voting
    result_data = Column(Text)  # JSON data for complex results
    calculated_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    proposal = relationship("Proposal", uselist=False)