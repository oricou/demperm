"""
Unit tests for DomainRepository, ForumRepository, SubforumRepository.

Tests cover:
- Domain CRUD operations
- Forum operations
- Subforum operations
- Repository methods
"""
import pytest
import uuid
from db.repositories.domain_repository import (
    DomainRepository,
    ForumRepository,
    SubforumRepository,
    MembershipRepository,
    SubforumSubscriptionRepository
)
from db.entities.domain_entity import Domain, Forum, Subforum, Membership


@pytest.mark.django_db
class TestDomainRepository:
    """Tests for DomainRepository methods."""

    def test_create_domain(self):
        """Test creating a domain."""
        domain = DomainRepository.create(
            domain_name='Test Domain',
            description='Test description',
            icon_url='https://example.com/icon.png'
        )

        assert domain is not None
        assert domain.domain_name == 'Test Domain'
        assert domain.description == 'Test description'
        assert domain.icon_url == 'https://example.com/icon.png'
        assert domain.subforum_count == 0
        assert domain.domain_id is not None

    def test_create_domain_minimal(self):
        """Test creating domain with minimal required fields."""
        domain = DomainRepository.create(domain_name='Minimal Domain')

        assert domain is not None
        assert domain.domain_name == 'Minimal Domain'
        assert domain.description is None
        assert domain.icon_url is None

    def test_get_all_domains_empty(self):
        """Test getting all domains when none exist."""
        domains = DomainRepository.get_all()

        assert isinstance(domains, list)
        assert len(domains) == 0

    def test_get_all_domains(self):
        """Test getting all domains."""
        # Create multiple domains
        DomainRepository.create(domain_name='Domain A')
        DomainRepository.create(domain_name='Domain B')
        DomainRepository.create(domain_name='Domain C')

        domains = DomainRepository.get_all()

        assert len(domains) == 3
        names = [d.domain_name for d in domains]
        assert 'Domain A' in names
        assert 'Domain B' in names
        assert 'Domain C' in names

    def test_get_all_domains_sorted_by_name(self):
        """Test domains are returned sorted by name."""
        DomainRepository.create(domain_name='Zeta')
        DomainRepository.create(domain_name='Alpha')
        DomainRepository.create(domain_name='Beta')

        domains = DomainRepository.get_all()

        names = [d.domain_name for d in domains]
        assert names == ['Alpha', 'Beta', 'Zeta']

    def test_get_by_id_success(self):
        """Test getting domain by ID successfully."""
        created = DomainRepository.create(domain_name='Test Domain')

        domain = DomainRepository.get_by_id(str(created.domain_id))

        assert domain is not None
        assert domain.domain_id == created.domain_id
        assert domain.domain_name == 'Test Domain'

    def test_get_by_id_not_found(self):
        """Test getting domain by non-existent ID returns None."""
        fake_id = str(uuid.uuid4())
        domain = DomainRepository.get_by_id(fake_id)

        assert domain is None

    def test_get_by_name_success(self):
        """Test getting domain by name successfully."""
        DomainRepository.create(domain_name='Unique Name')

        domain = DomainRepository.get_by_name('Unique Name')

        assert domain is not None
        assert domain.domain_name == 'Unique Name'

    def test_get_by_name_not_found(self):
        """Test getting domain by non-existent name returns None."""
        domain = DomainRepository.get_by_name('Non Existent')

        assert domain is None

    def test_get_by_name_case_sensitive(self):
        """Test domain name lookup is case sensitive."""
        DomainRepository.create(domain_name='TestDomain')

        domain = DomainRepository.get_by_name('testdomain')

        assert domain is None

    def test_update_domain_name(self):
        """Test updating domain name."""
        domain = DomainRepository.create(domain_name='Old Name')

        updated = DomainRepository.update(domain, domain_name='New Name')

        assert updated.domain_name == 'New Name'
        assert updated.domain_id == domain.domain_id

        # Verify in database
        domain.refresh_from_db()
        assert domain.domain_name == 'New Name'

    def test_update_domain_description(self):
        """Test updating domain description."""
        domain = DomainRepository.create(domain_name='Domain', description='Old description')

        updated = DomainRepository.update(domain, description='New description')

        assert updated.description == 'New description'

    def test_update_domain_icon_url(self):
        """Test updating domain icon URL."""
        domain = DomainRepository.create(domain_name='Domain')

        updated = DomainRepository.update(domain, icon_url='https://example.com/new.png')

        assert updated.icon_url == 'https://example.com/new.png'

    def test_update_domain_partial(self):
        """Test updating only some fields leaves others unchanged."""
        domain = DomainRepository.create(
            domain_name='Domain',
            description='Original',
            icon_url='https://example.com/icon.png'
        )

        updated = DomainRepository.update(domain, description='Updated')

        assert updated.domain_name == 'Domain'  # unchanged
        assert updated.description == 'Updated'  # changed
        assert updated.icon_url == 'https://example.com/icon.png'  # unchanged

    def test_update_domain_with_none_values(self):
        """Test updating domain with None doesn't change existing values."""
        domain = DomainRepository.create(
            domain_name='Domain',
            description='Description'
        )

        updated = DomainRepository.update(domain, domain_name=None, description=None)

        # None values should not update
        assert updated.domain_name == 'Domain'
        assert updated.description == 'Description'

    def test_delete_domain_success(self):
        """Test deleting domain successfully."""
        domain = DomainRepository.create(domain_name='To Delete')

        result = DomainRepository.delete(str(domain.domain_id))

        assert result is True

        # Verify deletion
        assert DomainRepository.get_by_id(str(domain.domain_id)) is None

    def test_delete_domain_not_found(self):
        """Test deleting non-existent domain returns False."""
        fake_id = str(uuid.uuid4())

        result = DomainRepository.delete(fake_id)

        assert result is False

    def test_increment_subforum_count(self):
        """Test incrementing subforum count."""
        domain = DomainRepository.create(domain_name='Domain')
        initial_count = domain.subforum_count

        DomainRepository.increment_subforum_count(str(domain.domain_id))

        # Refresh from database
        domain.refresh_from_db()
        assert domain.subforum_count == initial_count + 1

    def test_increment_subforum_count_multiple_times(self):
        """Test incrementing subforum count multiple times."""
        domain = DomainRepository.create(domain_name='Domain')

        DomainRepository.increment_subforum_count(str(domain.domain_id))
        DomainRepository.increment_subforum_count(str(domain.domain_id))
        DomainRepository.increment_subforum_count(str(domain.domain_id))

        domain.refresh_from_db()
        assert domain.subforum_count == 3


@pytest.mark.django_db
class TestForumRepository:
    """Tests for ForumRepository methods."""

    def test_create_forum(self, test_user):
        """Test creating a forum."""
        forum = ForumRepository.create(
            creator_id=str(test_user.user_id),
            forum_name='Test Forum',
            description='Test description',
            forum_image_url='https://example.com/image.png'
        )

        assert forum is not None
        assert forum.forum_name == 'Test Forum'
        assert forum.description == 'Test description'
        assert forum.forum_image_url == 'https://example.com/image.png'
        assert forum.creator_id == test_user.user_id
        assert forum.member_count == 0
        assert forum.post_count == 0

    def test_create_forum_minimal(self, test_user):
        """Test creating forum with minimal fields."""
        forum = ForumRepository.create(
            creator_id=str(test_user.user_id),
            forum_name='Minimal Forum'
        )

        assert forum is not None
        assert forum.forum_name == 'Minimal Forum'
        assert forum.description is None
        assert forum.forum_image_url is None

    def test_get_by_id_success(self, test_user):
        """Test getting forum by ID successfully."""
        created = ForumRepository.create(
            creator_id=str(test_user.user_id),
            forum_name='Test Forum'
        )

        forum = ForumRepository.get_by_id(str(created.forum_id))

        assert forum is not None
        assert forum.forum_id == created.forum_id
        assert forum.forum_name == 'Test Forum'

    def test_get_by_id_not_found(self):
        """Test getting forum by non-existent ID returns None."""
        fake_id = str(uuid.uuid4())
        forum = ForumRepository.get_by_id(fake_id)

        assert forum is None

    def test_get_all_forums(self, test_user):
        """Test getting all forums with pagination."""
        # Create multiple forums
        for i in range(5):
            ForumRepository.create(
                creator_id=str(test_user.user_id),
                forum_name=f'Forum {i}'
            )

        forums = ForumRepository.get_all(page=1, page_size=3)

        assert len(forums) == 3

    def test_get_all_forums_page_2(self, test_user):
        """Test getting second page of forums."""
        # Create 5 forums
        for i in range(5):
            ForumRepository.create(
                creator_id=str(test_user.user_id),
                forum_name=f'Forum {i}'
            )

        forums = ForumRepository.get_all(page=2, page_size=3)

        assert len(forums) == 2  # Remaining forums

    def test_search_forums(self, test_user):
        """Test searching forums by name."""
        ForumRepository.create(creator_id=str(test_user.user_id), forum_name='Alpha Forum')
        ForumRepository.create(creator_id=str(test_user.user_id), forum_name='Beta Forum')
        ForumRepository.create(creator_id=str(test_user.user_id), forum_name='Alpha Beta')

        results = ForumRepository.search('Alpha')

        assert len(results) == 2
        names = [f.forum_name for f in results]
        assert 'Alpha Forum' in names
        assert 'Alpha Beta' in names

    def test_search_forums_case_insensitive(self, test_user):
        """Test forum search is case insensitive."""
        ForumRepository.create(creator_id=str(test_user.user_id), forum_name='TestForum')

        results = ForumRepository.search('testforum')

        assert len(results) == 1
        assert results[0].forum_name == 'TestForum'

    def test_increment_member_count(self, test_user):
        """Test incrementing member count."""
        forum = ForumRepository.create(
            creator_id=str(test_user.user_id),
            forum_name='Forum'
        )

        ForumRepository.increment_member_count(str(forum.forum_id))

        forum.refresh_from_db()
        assert forum.member_count == 1

    def test_decrement_member_count(self, test_user):
        """Test decrementing member count."""
        forum = ForumRepository.create(
            creator_id=str(test_user.user_id),
            forum_name='Forum'
        )
        forum.member_count = 5
        forum.save()

        ForumRepository.decrement_member_count(str(forum.forum_id))

        forum.refresh_from_db()
        assert forum.member_count == 4

    def test_increment_post_count(self, test_user):
        """Test incrementing post count."""
        forum = ForumRepository.create(
            creator_id=str(test_user.user_id),
            forum_name='Forum'
        )

        ForumRepository.increment_post_count(str(forum.forum_id))

        forum.refresh_from_db()
        assert forum.post_count == 1


@pytest.mark.django_db
class TestSubforumRepository:
    """Tests for SubforumRepository methods."""

    def test_create_subforum_with_auto_forum(self, test_user):
        """Test creating subforum automatically creates a forum."""
        subforum = SubforumRepository.create(
            creator_id=str(test_user.user_id),
            subforum_name='Test Subforum',
            description='Test description'
        )

        assert subforum is not None
        assert subforum.subforum_name == 'Test Subforum'
        assert subforum.description == 'Test description'
        assert subforum.forum_id is not None  # Auto-created forum

        # Verify forum was created
        forum = Forum.objects.get(forum_id=subforum.forum_id.forum_id)
        assert forum.forum_name == 'Test Subforum'

    def test_create_subforum_in_domain(self, test_user):
        """Test creating subforum in a domain."""
        domain = Domain.objects.create(domain_name='Test Domain')

        subforum = SubforumRepository.create(
            creator_id=str(test_user.user_id),
            subforum_name='Domain Subforum',
            description='In domain',
            parent_domain_id=str(domain.domain_id)
        )

        assert subforum.parent_domain_id == domain.domain_id
        assert subforum.parent_forum_id is None

    def test_create_subforum_in_forum(self, test_user):
        """Test creating subforum as child of another forum."""
        parent_forum = ForumRepository.create(
            creator_id=str(test_user.user_id),
            forum_name='Parent Forum'
        )

        subforum = SubforumRepository.create(
            creator_id=str(test_user.user_id),
            subforum_name='Child Subforum',
            description='In forum',
            parent_forum_id=str(parent_forum.forum_id)
        )

        assert subforum.parent_forum_id == parent_forum.forum_id
        assert subforum.parent_domain_id is None

    def test_create_subforum_with_existing_forum_id(self, test_user):
        """Test creating subforum attached to existing forum."""
        existing_forum = ForumRepository.create(
            creator_id=str(test_user.user_id),
            forum_name='Existing Forum'
        )

        subforum = SubforumRepository.create(
            creator_id=str(test_user.user_id),
            subforum_name='Subforum',
            forum_id=str(existing_forum.forum_id)
        )

        assert subforum.forum_id == existing_forum

    def test_get_by_id_success(self, test_user):
        """Test getting subforum by ID successfully."""
        created = SubforumRepository.create(
            creator_id=str(test_user.user_id),
            subforum_name='Test Subforum'
        )

        subforum = SubforumRepository.get_by_id(str(created.subforum_id))

        assert subforum is not None
        assert subforum.subforum_id == created.subforum_id

    def test_get_by_id_not_found(self):
        """Test getting subforum by non-existent ID returns None."""
        fake_id = str(uuid.uuid4())
        subforum = SubforumRepository.get_by_id(fake_id)

        assert subforum is None

    def test_get_by_domain(self, test_user):
        """Test getting subforums by domain."""
        domain = Domain.objects.create(domain_name='Domain')

        # Create subforums in domain
        SubforumRepository.create(
            creator_id=str(test_user.user_id),
            subforum_name='Subforum 1',
            parent_domain_id=str(domain.domain_id)
        )
        SubforumRepository.create(
            creator_id=str(test_user.user_id),
            subforum_name='Subforum 2',
            parent_domain_id=str(domain.domain_id)
        )

        # Create subforum in different domain (should not be returned)
        other_domain = Domain.objects.create(domain_name='Other Domain')
        SubforumRepository.create(
            creator_id=str(test_user.user_id),
            subforum_name='Other Subforum',
            parent_domain_id=str(other_domain.domain_id)
        )

        subforums = SubforumRepository.get_by_domain(str(domain.domain_id))

        assert len(subforums) == 2
        names = [s.subforum_name for s in subforums]
        assert 'Subforum 1' in names
        assert 'Subforum 2' in names

    def test_get_by_domain_pagination(self, test_user):
        """Test pagination when getting subforums by domain."""
        domain = Domain.objects.create(domain_name='Domain')

        # Create 5 subforums
        for i in range(5):
            SubforumRepository.create(
                creator_id=str(test_user.user_id),
                subforum_name=f'Subforum {i}',
                parent_domain_id=str(domain.domain_id)
            )

        # Get page 1
        page1 = SubforumRepository.get_by_domain(str(domain.domain_id), page=1, page_size=2)
        assert len(page1) == 2

        # Get page 2
        page2 = SubforumRepository.get_by_domain(str(domain.domain_id), page=2, page_size=2)
        assert len(page2) == 2

    def test_get_by_forum(self, test_user):
        """Test getting subforums by parent forum."""
        parent_forum = ForumRepository.create(
            creator_id=str(test_user.user_id),
            forum_name='Parent Forum'
        )

        # Create subforums in parent forum
        SubforumRepository.create(
            creator_id=str(test_user.user_id),
            subforum_name='Child 1',
            parent_forum_id=str(parent_forum.forum_id)
        )
        SubforumRepository.create(
            creator_id=str(test_user.user_id),
            subforum_name='Child 2',
            parent_forum_id=str(parent_forum.forum_id)
        )

        subforums = SubforumRepository.get_by_forum(str(parent_forum.forum_id))

        assert len(subforums) == 2

    def test_increment_post_count(self, test_user):
        """Test incrementing subforum post count."""
        subforum = SubforumRepository.create(
            creator_id=str(test_user.user_id),
            subforum_name='Subforum'
        )

        SubforumRepository.increment_post_count(str(subforum.subforum_id))

        subforum.refresh_from_db()
        assert subforum.post_count == 1

    def test_decrement_post_count(self, test_user):
        """Test decrementing subforum post count."""
        subforum = SubforumRepository.create(
            creator_id=str(test_user.user_id),
            subforum_name='Subforum'
        )
        subforum.post_count = 5
        subforum.save()

        SubforumRepository.decrement_post_count(str(subforum.subforum_id))

        subforum.refresh_from_db()
        assert subforum.post_count == 4


@pytest.mark.django_db
class TestMembershipRepository:
    """Tests for MembershipRepository methods."""

    def test_create_membership(self, test_user):
        """Test creating a membership."""
        forum = ForumRepository.create(
            creator_id=str(test_user.user_id),
            forum_name='Forum'
        )

        membership = MembershipRepository.create(
            user_id=str(test_user.user_id),
            forum_id=str(forum.forum_id),
            role='member'
        )

        assert membership is not None
        assert membership.user_id == test_user.user_id
        assert membership.forum_id == forum.forum_id
        assert membership.role == 'member'

    def test_create_membership_default_role(self, test_user):
        """Test creating membership with default role."""
        forum = ForumRepository.create(
            creator_id=str(test_user.user_id),
            forum_name='Forum'
        )

        membership = MembershipRepository.create(
            user_id=str(test_user.user_id),
            forum_id=str(forum.forum_id)
        )

        assert membership.role == 'member'

    def test_delete_membership(self, test_user):
        """Test deleting a membership."""
        forum = ForumRepository.create(
            creator_id=str(test_user.user_id),
            forum_name='Forum'
        )

        MembershipRepository.create(
            user_id=str(test_user.user_id),
            forum_id=str(forum.forum_id)
        )

        result = MembershipRepository.delete(
            user_id=str(test_user.user_id),
            forum_id=str(forum.forum_id)
        )

        assert result is True
        assert not MembershipRepository.exists(
            str(test_user.user_id),
            str(forum.forum_id)
        )

    def test_exists_membership(self, test_user):
        """Test checking if membership exists."""
        forum = ForumRepository.create(
            creator_id=str(test_user.user_id),
            forum_name='Forum'
        )

        # Should not exist initially
        assert not MembershipRepository.exists(
            str(test_user.user_id),
            str(forum.forum_id)
        )

        # Create membership
        MembershipRepository.create(
            user_id=str(test_user.user_id),
            forum_id=str(forum.forum_id)
        )

        # Should exist now
        assert MembershipRepository.exists(
            str(test_user.user_id),
            str(forum.forum_id)
        )

    def test_get_user_forums(self, test_user):
        """Test getting forums a user is member of."""
        # Create multiple forums and memberships
        forum1 = ForumRepository.create(
            creator_id=str(test_user.user_id),
            forum_name='Forum 1'
        )
        forum2 = ForumRepository.create(
            creator_id=str(test_user.user_id),
            forum_name='Forum 2'
        )

        MembershipRepository.create(
            user_id=str(test_user.user_id),
            forum_id=str(forum1.forum_id)
        )
        MembershipRepository.create(
            user_id=str(test_user.user_id),
            forum_id=str(forum2.forum_id)
        )

        memberships = MembershipRepository.get_user_forums(str(test_user.user_id))

        assert len(memberships) == 2


@pytest.mark.django_db
class TestSubforumSubscriptionRepository:
    """Tests for SubforumSubscriptionRepository methods."""

    def test_create_subscription(self, test_user):
        """Test creating a subforum subscription."""
        subforum = SubforumRepository.create(
            creator_id=str(test_user.user_id),
            subforum_name='Subforum'
        )

        subscription = SubforumSubscriptionRepository.create(
            user_id=str(test_user.user_id),
            subforum_id=str(subforum.subforum_id)
        )

        assert subscription is not None
        assert subscription.user_id == test_user.user_id
        assert subscription.subforum_id == subforum.subforum_id

    def test_delete_subscription(self, test_user):
        """Test deleting a subforum subscription."""
        subforum = SubforumRepository.create(
            creator_id=str(test_user.user_id),
            subforum_name='Subforum'
        )

        SubforumSubscriptionRepository.create(
            user_id=str(test_user.user_id),
            subforum_id=str(subforum.subforum_id)
        )

        result = SubforumSubscriptionRepository.delete(
            user_id=str(test_user.user_id),
            subforum_id=str(subforum.subforum_id)
        )

        assert result is True

    def test_exists_subscription(self, test_user):
        """Test checking if subscription exists."""
        subforum = SubforumRepository.create(
            creator_id=str(test_user.user_id),
            subforum_name='Subforum'
        )

        # Should not exist initially
        assert not SubforumSubscriptionRepository.exists(
            str(test_user.user_id),
            str(subforum.subforum_id)
        )

        # Create subscription
        SubforumSubscriptionRepository.create(
            user_id=str(test_user.user_id),
            subforum_id=str(subforum.subforum_id)
        )

        # Should exist now
        assert SubforumSubscriptionRepository.exists(
            str(test_user.user_id),
            str(subforum.subforum_id)
        )

    def test_get_user_subforums(self, test_user):
        """Test getting subforums a user is subscribed to."""
        # Create multiple subforums and subscriptions
        subforum1 = SubforumRepository.create(
            creator_id=str(test_user.user_id),
            subforum_name='Subforum 1'
        )
        subforum2 = SubforumRepository.create(
            creator_id=str(test_user.user_id),
            subforum_name='Subforum 2'
        )

        SubforumSubscriptionRepository.create(
            user_id=str(test_user.user_id),
            subforum_id=str(subforum1.subforum_id)
        )
        SubforumSubscriptionRepository.create(
            user_id=str(test_user.user_id),
            subforum_id=str(subforum2.subforum_id)
        )

        subscriptions = SubforumSubscriptionRepository.get_user_subforums(str(test_user.user_id))

        assert len(subscriptions) == 2
