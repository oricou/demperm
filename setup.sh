#!/bin/bash

# Startup script for Démocratie Permanente

echo "=== Démocratie Permanente - Startup Script ==="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

# Check if we're in a virtual environment
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "Warning: Not in a virtual environment. Creating one..."
    python3 -m venv venv
    source venv/bin/activate
    echo "Virtual environment created and activated"
fi

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "Please edit .env file with your configuration"
fi

# Initialize database
echo "Initializing database..."
if [ ! -f demperm.db ]; then
    # Generate initial migration
    alembic revision --autogenerate -m "Initial migration"
fi

# Run migrations
alembic upgrade head

# Create a default admin user if it doesn't exist
python3 -c "
from demperm.database import SessionLocal
from demperm.models import User, UserRole
from demperm.auth import get_password_hash

db = SessionLocal()
admin = db.query(User).filter(User.username == 'admin').first()
if not admin:
    admin = User(
        username='admin',
        email='admin@democrariepermanente.fr',
        full_name='Administrateur',
        hashed_password=get_password_hash('admin123'),
        role=UserRole.ADMINISTRATOR,
        is_verified=True
    )
    db.add(admin)
    db.commit()
    print('Default admin user created: admin/admin123')
else:
    print('Admin user already exists')
db.close()
"

echo "=== Setup complete! ==="
echo "You can now start the application with:"
echo "  python -m demperm.main"
echo ""
echo "Or start with uvicorn for development:"
echo "  uvicorn demperm.main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "Access the application at: http://localhost:8000"
echo "API documentation at: http://localhost:8000/docs"