"""Main FastAPI application for the democracy platform."""

from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from datetime import timedelta
import os

from .database import get_db
from .models import User, Proposal, Category, Vote, Comment
from .schemas import (
    UserCreate, User as UserSchema, Token,
    ProposalCreate, Proposal as ProposalSchema,
    CategoryCreate, Category as CategorySchema,
    VoteCreate, Vote as VoteSchema,
    CommentCreate, Comment as CommentSchema,
    DashboardStats
)
from .auth import (
    authenticate_user, create_access_token, get_current_active_user,
    get_password_hash, ACCESS_TOKEN_EXPIRE_MINUTES
)

app = FastAPI(
    title="Démocratie Permanente",
    description="Platform for continuous democratic participation and decision-making",
    version="0.1.0"
)

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, db: Session = Depends(get_db)):
    """Dashboard page."""
    # Get basic statistics
    total_users = db.query(User).count()
    active_proposals = db.query(Proposal).filter(
        Proposal.status.in_(["discussion", "voting"])
    ).count()
    total_votes = db.query(Vote).count()
    
    recent_proposals = db.query(Proposal).order_by(
        Proposal.created_at.desc()
    ).limit(5).all()
    
    stats = {
        "total_users": total_users,
        "active_proposals": active_proposals,
        "total_votes": total_votes,
        "recent_proposals": recent_proposals
    }
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "stats": stats
    })


# Authentication endpoints
@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Authenticate user and return access token."""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/register", response_model=UserSchema)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    # Check if user already exists
    db_user = db.query(User).filter(
        (User.username == user.username) | (User.email == user.email)
    ).first()
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Username or email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.get("/users/me", response_model=UserSchema)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """Get current user information."""
    return current_user


# Proposal endpoints
@app.post("/proposals", response_model=ProposalSchema)
async def create_proposal(
    proposal: ProposalCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new proposal."""
    db_proposal = Proposal(
        title=proposal.title,
        description=proposal.description,
        content=proposal.content,
        vote_type=proposal.vote_type,
        category_id=proposal.category_id,
        author_id=current_user.id
    )
    db.add(db_proposal)
    db.commit()
    db.refresh(db_proposal)
    return db_proposal


@app.get("/proposals", response_model=list[ProposalSchema])
async def list_proposals(
    skip: int = 0,
    limit: int = 100,
    status: str = None,
    category_id: int = None,
    db: Session = Depends(get_db)
):
    """List proposals with optional filtering."""
    query = db.query(Proposal)
    
    if status:
        query = query.filter(Proposal.status == status)
    if category_id:
        query = query.filter(Proposal.category_id == category_id)
    
    proposals = query.offset(skip).limit(limit).all()
    return proposals


@app.get("/proposals/{proposal_id}", response_model=ProposalSchema)
async def get_proposal(proposal_id: int, db: Session = Depends(get_db)):
    """Get a specific proposal."""
    proposal = db.query(Proposal).filter(Proposal.id == proposal_id).first()
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")
    return proposal


# Vote endpoints
@app.post("/votes", response_model=VoteSchema)
async def cast_vote(
    vote: VoteCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Cast a vote on a proposal."""
    # Check if proposal exists and is in voting phase
    proposal = db.query(Proposal).filter(Proposal.id == vote.proposal_id).first()
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")
    
    if proposal.status != "voting":
        raise HTTPException(status_code=400, detail="Proposal is not in voting phase")
    
    # Check if user has already voted
    existing_vote = db.query(Vote).filter(
        Vote.user_id == current_user.id,
        Vote.proposal_id == vote.proposal_id
    ).first()
    
    if existing_vote:
        # Update existing vote
        existing_vote.value = vote.value
        existing_vote.comment = vote.comment
        db.commit()
        db.refresh(existing_vote)
        return existing_vote
    else:
        # Create new vote
        db_vote = Vote(
            value=vote.value,
            comment=vote.comment,
            user_id=current_user.id,
            proposal_id=vote.proposal_id
        )
        db.add(db_vote)
        db.commit()
        db.refresh(db_vote)
        return db_vote


# Category endpoints
@app.post("/categories", response_model=CategorySchema)
async def create_category(
    category: CategoryCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new category."""
    if current_user.role.value not in ["moderator", "administrator"]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    db_category = Category(
        name=category.name,
        description=category.description,
        color=category.color
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


@app.get("/categories", response_model=list[CategorySchema])
async def list_categories(db: Session = Depends(get_db)):
    """List all categories."""
    categories = db.query(Category).all()
    return categories


# Comment endpoints
@app.post("/comments", response_model=CommentSchema)
async def create_comment(
    comment: CommentCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a comment on a proposal."""
    # Check if proposal exists
    proposal = db.query(Proposal).filter(Proposal.id == comment.proposal_id).first()
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")
    
    db_comment = Comment(
        content=comment.content,
        author_id=current_user.id,
        proposal_id=comment.proposal_id,
        parent_id=comment.parent_id
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


@app.get("/proposals/{proposal_id}/comments", response_model=list[CommentSchema])
async def list_proposal_comments(
    proposal_id: int,
    db: Session = Depends(get_db)
):
    """List comments for a proposal."""
    comments = db.query(Comment).filter(
        Comment.proposal_id == proposal_id,
        Comment.is_deleted == False
    ).order_by(Comment.created_at).all()
    return comments


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)