#!/usr/bin/env python3
"""Initialize the database with tables and sample data."""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath('.'))

from demperm.database import engine, create_tables
from demperm.models import Base, User, Category, Proposal, UserRole, ProposalStatus, VoteType
from demperm.auth import get_password_hash
from sqlalchemy.orm import sessionmaker

def init_database():
    """Initialize the database with tables and sample data."""
    print("Creating database tables...")
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create a session
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Check if we already have data
        if db.query(User).count() > 0:
            print("Database already has data. Skipping initialization.")
            return
        
        print("Adding sample data...")
        
        # Create sample users
        admin_user = User(
            username="admin",
            email="admin@democrariepermanente.fr",
            full_name="Administrateur",
            hashed_password=get_password_hash("admin123"),
            role=UserRole.ADMINISTRATOR,
            is_verified=True
        )
        
        demo_user = User(
            username="demo",
            email="demo@democrariepermanente.fr",
            full_name="Utilisateur Démo",
            hashed_password=get_password_hash("demo123"),
            role=UserRole.CITIZEN,
            is_verified=True
        )
        
        db.add(admin_user)
        db.add(demo_user)
        db.commit()
        db.refresh(admin_user)
        db.refresh(demo_user)
        
        # Create sample categories
        categories = [
            Category(name="Environnement", description="Propositions liées à l'environnement et au développement durable", color="#28a745"),
            Category(name="Économie", description="Propositions économiques et financières", color="#007bff"),
            Category(name="Social", description="Propositions sociales et sociétales", color="#dc3545"),
            Category(name="Infrastructure", description="Propositions d'infrastructure et d'aménagement", color="#ffc107"),
            Category(name="Éducation", description="Propositions liées à l'éducation et à la formation", color="#17a2b8")
        ]
        
        for category in categories:
            db.add(category)
        
        db.commit()
        
        # Create sample proposals
        env_category = db.query(Category).filter(Category.name == "Environnement").first()
        social_category = db.query(Category).filter(Category.name == "Social").first()
        
        sample_proposals = [
            Proposal(
                title="Installation de panneaux solaires sur les bâtiments publics",
                description="Proposer l'installation de panneaux solaires sur tous les bâtiments publics de la commune pour réduire l'empreinte carbone et les coûts énergétiques.",
                content="Cette proposition vise à équiper tous les bâtiments publics (mairie, écoles, centres communaux) de panneaux solaires photovoltaïques. L'investissement initial serait compensé par les économies d'énergie à long terme et la vente du surplus d'électricité. Cette initiative s'inscrit dans une démarche de transition énergétique et de lutte contre le changement climatique.",
                status=ProposalStatus.DISCUSSION,
                vote_type=VoteType.YES_NO,
                author_id=demo_user.id,
                category_id=env_category.id
            ),
            Proposal(
                title="Création d'un jardin communautaire",
                description="Développer un espace de jardinage partagé pour renforcer les liens sociaux et promouvoir l'agriculture urbaine.",
                content="Ce projet propose la création d'un jardin communautaire où les habitants pourront cultiver leurs propres légumes et fruits. L'espace inclurait des parcelles individuelles et collectives, un compost commun, et des ateliers d'initiation au jardinage. Cette initiative favoriserait les échanges intergénérationnels, l'éducation environnementale et l'accès à une alimentation saine et locale.",
                status=ProposalStatus.VOTING,
                vote_type=VoteType.APPROVAL,
                author_id=admin_user.id,
                category_id=social_category.id
            ),
            Proposal(
                title="Mise en place d'un système de covoiturage municipal",
                description="Organiser un système de covoiturage pour réduire le trafic et les émissions de CO2.",
                content="Cette proposition consiste à mettre en place une plateforme de covoiturage dédiée aux habitants de la commune. Le système inclurait une application mobile, des points de rendez-vous sécurisés, et des incitations financières pour les participants. L'objectif est de réduire le nombre de véhicules individuels en circulation, diminuer les embouteillages et favoriser les rencontres entre citoyens.",
                status=ProposalStatus.DRAFT,
                vote_type=VoteType.SCORE,
                author_id=demo_user.id,
                category_id=env_category.id
            )
        ]
        
        for proposal in sample_proposals:
            db.add(proposal)
        
        db.commit()
        
        print("Database initialized successfully!")
        print("Sample users created:")
        print("  - Admin: admin / admin123")
        print("  - Demo: demo / demo123")
        print("Sample categories and proposals have been added.")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_database()