"""
Domain and Forum repository for data access.
"""
from typing import Optional, List
from django.db.models import F
from db.entities.domain_entity import Domain, Forum, Subforum, Membership


class DomainRepository:
    """Repository for Domain entity operations."""
    
    @staticmethod
    def get_all() -> List[Domain]:
        """Get all domains."""
        return Domain.objects.all().order_by('domain_name')
    
    @staticmethod
    def get_by_id(domain_id: str) -> Optional[Domain]:
        """Get domain by ID."""
        try:
            return Domain.objects.get(domain_id=domain_id)
        except Domain.DoesNotExist:
            return None
    
    @staticmethod
    def get_by_name(domain_name: str) -> Optional[Domain]:
        """Get domain by name."""
        try:
            return Domain.objects.get(domain_name=domain_name)
        except Domain.DoesNotExist:
            return None
    
    @staticmethod
    def create(domain_name: str, description: Optional[str] = None, icon_url: Optional[str] = None) -> Domain:
        """Create a new domain."""
        return Domain.objects.create(
            domain_name=domain_name,
            description=description,
            icon_url=icon_url
        )

    @staticmethod
    def update(domain: Domain, domain_name: Optional[str] = None,
               description: Optional[str] = None, icon_url: Optional[str] = None) -> Domain:
        """Update an existing domain instance and persist changes."""
        if domain_name is not None:
            domain.domain_name = domain_name
        if description is not None:
            domain.description = description
        if icon_url is not None:
            domain.icon_url = icon_url
        domain.save()
        return domain

    @staticmethod
    def delete(domain_id: str) -> bool:
        """Delete a domain by id. Returns True if a row was removed."""
        deleted, _ = Domain.objects.filter(domain_id=domain_id).delete()
        return deleted > 0
    
    @staticmethod
    def increment_subforum_count(domain_id: str) -> None:
        """Increment subforum count."""
        Domain.objects.filter(domain_id=domain_id).update(subforum_count=F('subforum_count') + 1)


class ForumRepository:
    """Repository for Forum entity operations."""
    
    @staticmethod
    def create(creator_id: str, forum_name: str, description: Optional[str] = None, 
               forum_image_url: Optional[str] = None) -> Forum:
        """Create a new forum."""
        return Forum.objects.create(
            creator_id=creator_id,
            forum_name=forum_name,
            description=description,
            forum_image_url=forum_image_url
        )
    
    @staticmethod
    def get_by_id(forum_id: str) -> Optional[Forum]:
        """Get forum by ID."""
        try:
            return Forum.objects.select_related('creator').get(forum_id=forum_id)
        except Forum.DoesNotExist:
            return None
    
    @staticmethod
    def get_all(page: int = 1, page_size: int = 20) -> List[Forum]:
        """Get all forums."""
        offset = (page - 1) * page_size
        return Forum.objects.select_related('creator').order_by('-created_at')[offset:offset + page_size]
    
    @staticmethod
    def search(query: str, page: int = 1, page_size: int = 20) -> List[Forum]:
        """Search forums by name."""
        offset = (page - 1) * page_size
        return Forum.objects.filter(forum_name__icontains=query).select_related('creator')[offset:offset + page_size]
    
    @staticmethod
    def increment_member_count(forum_id: str) -> None:
        """Increment member count."""
        Forum.objects.filter(forum_id=forum_id).update(member_count=F('member_count') + 1)
    
    @staticmethod
    def decrement_member_count(forum_id: str) -> None:
        """Decrement member count."""
        Forum.objects.filter(forum_id=forum_id).update(member_count=F('member_count') - 1)
    
    @staticmethod
    def increment_post_count(forum_id: str) -> None:
        """Increment post count."""
        Forum.objects.filter(forum_id=forum_id).update(post_count=F('post_count') + 1)


class SubforumRepository:
    """Repository for Subforum entity operations."""
    
    @staticmethod
    def create(creator_id: str, subforum_name: str, description: Optional[str] = None,
               parent_domain_id: Optional[str] = None, parent_forum_id: Optional[str] = None) -> Subforum:
        """Create a new subforum."""
        return Subforum.objects.create(
            creator_id=creator_id,
            subforum_name=subforum_name,
            description=description,
            parent_domain_id=parent_domain_id,
            parent_forum_id=parent_forum_id
        )
    
    @staticmethod
    def get_by_id(subforum_id: str) -> Optional[Subforum]:
        """Get subforum by ID."""
        try:
            return Subforum.objects.select_related('creator', 'parent_domain', 'parent_forum').get(subforum_id=subforum_id)
        except Subforum.DoesNotExist:
            return None
    
    @staticmethod
    def get_by_domain(domain_id: str, page: int = 1, page_size: int = 20) -> List[Subforum]:
        """Get subforums by domain."""
        offset = (page - 1) * page_size
        return Subforum.objects.filter(parent_domain_id=domain_id).select_related('creator')[offset:offset + page_size]
    
    @staticmethod
    def get_by_forum(forum_id: str, page: int = 1, page_size: int = 20) -> List[Subforum]:
        """Get subforums by forum."""
        offset = (page - 1) * page_size
        return Subforum.objects.filter(parent_forum_id=forum_id).select_related('creator')[offset:offset + page_size]
    
    @staticmethod
    def increment_post_count(subforum_id: str) -> None:
        """Increment post count."""
        Subforum.objects.filter(subforum_id=subforum_id).update(post_count=F('post_count') + 1)


class MembershipRepository:
    """Repository for Membership entity operations."""
    
    @staticmethod
    def create(user_id: str, forum_id: str, role: str = 'member') -> Membership:
        """Create a membership."""
        return Membership.objects.create(user_id=user_id, forum_id=forum_id, role=role)
    
    @staticmethod
    def delete(user_id: str, forum_id: str) -> bool:
        """Delete a membership."""
        deleted, _ = Membership.objects.filter(user_id=user_id, forum_id=forum_id).delete()
        return deleted > 0
    
    @staticmethod
    def exists(user_id: str, forum_id: str) -> bool:
        """Check if membership exists."""
        return Membership.objects.filter(user_id=user_id, forum_id=forum_id).exists()
    
    @staticmethod
    def get_user_forums(user_id: str, page: int = 1, page_size: int = 20) -> List[Membership]:
        """Get forums user is member of."""
        offset = (page - 1) * page_size
        return Membership.objects.filter(user_id=user_id).select_related('forum')[offset:offset + page_size]


class SubforumSubscriptionRepository:
    """Repository for subforum subscriptions."""

    @staticmethod
    def create(user_id: str, subforum_id: str):
        """Create a subforum subscription."""
        from db.entities.domain_entity import SubforumSubscription
        return SubforumSubscription.objects.create(user_id=user_id, subforum_id=subforum_id)

    @staticmethod
    def delete(user_id: str, subforum_id: str) -> bool:
        """Delete a subforum subscription."""
        from db.entities.domain_entity import SubforumSubscription
        deleted, _ = SubforumSubscription.objects.filter(user_id=user_id, subforum_id=subforum_id).delete()
        return deleted > 0

    @staticmethod
    def exists(user_id: str, subforum_id: str) -> bool:
        """Check if subscription exists."""
        from db.entities.domain_entity import SubforumSubscription
        return SubforumSubscription.objects.filter(user_id=user_id, subforum_id=subforum_id).exists()

    @staticmethod
    def get_user_subforums(user_id: str, page: int = 1, page_size: int = 20):
        """Get subforums a user is subscribed to."""
        from db.entities.domain_entity import SubforumSubscription
        offset = (page - 1) * page_size
        return SubforumSubscription.objects.filter(user_id=user_id).select_related('subforum')[offset:offset + page_size]

