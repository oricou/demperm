"""Database configuration and setup."""

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from decouple import config, Config, RepositoryEnv

# Try to read from .env file, fall back to environment variables
try:
    config_obj = Config(RepositoryEnv('.env'))
    DATABASE_URL = config_obj.get("DATABASE_URL", default="sqlite:///./demperm.db")
except:
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./demperm.db")

# SQLAlchemy setup
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

metadata = MetaData()


def get_db():
    """Dependency to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """Create database tables."""
    Base.metadata.create_all(bind=engine)