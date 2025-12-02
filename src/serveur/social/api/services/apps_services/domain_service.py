"""
Domain and subforum service.
"""
from typing import List, Optional
from django.db import transaction
from db.repositories.domain_repository import DomainRepository, SubforumRepository
from db.repositories.message_repository import AuditLogRepository
from db.entities.domain_entity import Domain, Subforum
from common.exceptions import NotFoundError, ValidationError
from common.validators import Validator
from django.db import IntegrityError


class DomainService:
    """Service for domain and subforum management."""
    
    @staticmethod
    def get_all_domains() -> List[Domain]:
        """Get all 9 political domains."""
        return DomainRepository.get_all()
    
    @staticmethod
    def get_domain_by_id(domain_id: str) -> Domain:
        """Get domain by ID."""
        domain = DomainRepository.get_by_id(domain_id)
        if not domain:
            raise NotFoundError(f"Domain {domain_id} not found")
        return domain
    
    @staticmethod
    def get_domain_by_name(name: str) -> Domain:
        """Get domain by name."""
        domain = DomainRepository.get_by_name(name)
        if not domain:
            raise NotFoundError(f"Domain '{name}' not found")
        return domain
    
    @staticmethod
    def get_domain_subforums(domain_id: str, page: int = 1, page_size: int = 20) -> List[Subforum]:
        """Get subforums for a domain."""
        # Check domain exists
        domain = DomainService.get_domain_by_id(domain_id)
        
        return SubforumRepository.get_by_domain(domain_id, page, page_size)
    
    @staticmethod
    @transaction.atomic
    def create_subforum_in_domain(
        user_id: str,
        domain_id: str,
        name: str,
        description: str,
        ip_address: Optional[str] = None
    ) -> Subforum:
        """
        Create a subforum in a domain.
        
        Args:
            user_id: User ID (creator)
            domain_id: Domain ID
            name: Subforum name
            description: Subforum description
            ip_address: Client IP address
            
        Returns:
            Created subforum
        """
        # Validate
        name = Validator.validate_forum_name(name)
        description = Validator.validate_description(description)
        
        # Check domain exists
        domain = DomainService.get_domain_by_id(domain_id)
        
        # Create subforum
        subforum = SubforumRepository.create(
            creator_id=user_id,
            subforum_name=name,
            description=description,
            parent_domain_id=domain_id,
            parent_forum_id=None
        )
        
        # Increment domain subforum count
        DomainRepository.increment_subforum_count(domain_id)
        
        # Audit log
        AuditLogRepository.create(
            user_id=user_id,
            action_type='subforum_created',
            resource_type='subforum',
            resource_id=str(subforum.subforum_id),
            details={'domain_id': domain_id},
            ip_address=ip_address
        )
        
        return subforum
    
    @staticmethod
    def get_subforum_by_id(subforum_id: str) -> Subforum:
        """Get subforum by ID."""
        subforum = SubforumRepository.get_by_id(subforum_id)
        if not subforum:
            raise NotFoundError(f"Subforum {subforum_id} not found")
        return subforum

    # Admin operations
    @staticmethod
    @transaction.atomic
    def create_domain(admin_id: str, domain_name: str, description: Optional[str] = None,
                      icon_url: Optional[str] = None, ip_address: Optional[str] = None) -> Domain:
        """Create a domain (admin only)."""
        domain_name = Validator.validate_forum_name(domain_name)
        if len(domain_name) > 100:
            raise ValidationError("Domain name must be 3-100 characters")
        if description is not None:
            description = Validator.validate_description(description, max_length=1000)

        if DomainRepository.get_by_name(domain_name):
            raise ValidationError("Domain name already exists")

        try:
            domain = DomainRepository.create(domain_name=domain_name, description=description, icon_url=icon_url)
        except IntegrityError as exc:
            raise ValidationError("Could not create domain") from exc

        AuditLogRepository.create(
            user_id=admin_id,
            action_type='create',
            resource_type='domain',
            resource_id=str(domain.domain_id),
            details={'domain_name': domain_name},
            ip_address=ip_address
        )
        return domain

    @staticmethod
    @transaction.atomic
    def update_domain(admin_id: str, domain_id: str, domain_name: Optional[str] = None,
                      description: Optional[str] = None, icon_url: Optional[str] = None,
                      ip_address: Optional[str] = None) -> Domain:
        """Update a domain (admin only)."""
        domain = DomainService.get_domain_by_id(domain_id)

        if domain_name:
            domain_name = Validator.validate_forum_name(domain_name)
            if len(domain_name) > 100:
                raise ValidationError("Domain name must be 3-100 characters")
            existing = DomainRepository.get_by_name(domain_name)
            if existing and str(existing.domain_id) != str(domain_id):
                raise ValidationError("Domain name already exists")
        if description is not None:
            description = Validator.validate_description(description, max_length=1000)

        domain = DomainRepository.update(domain, domain_name=domain_name, description=description, icon_url=icon_url)

        AuditLogRepository.create(
            user_id=admin_id,
            action_type='update',
            resource_type='domain',
            resource_id=str(domain.domain_id),
            details={'domain_name': domain.domain_name},
            ip_address=ip_address
        )
        return domain

    @staticmethod
    @transaction.atomic
    def delete_domain(admin_id: str, domain_id: str, ip_address: Optional[str] = None) -> None:
        """Delete a domain (admin only)."""
        domain = DomainService.get_domain_by_id(domain_id)
        deleted = DomainRepository.delete(domain_id)
        if not deleted:
            raise NotFoundError(f"Domain {domain_id} not found")

        AuditLogRepository.create(
            user_id=admin_id,
            action_type='delete',
            resource_type='domain',
            resource_id=str(domain.domain_id),
            details={'domain_name': domain.domain_name},
            ip_address=ip_address
        )

