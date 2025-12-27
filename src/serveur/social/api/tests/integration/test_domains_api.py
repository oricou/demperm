"""
Integration tests for domains API endpoints.

Tests cover:
- Listing all 9 political domains
- Getting domain details
- Getting subforums for a domain
- Creating subforums in a domain
- Permissions and access control
"""
import pytest
import uuid
from rest_framework.test import APIClient
from db.entities.domain_entity import Domain, Subforum


@pytest.mark.django_db
class TestDomainsListAPI:
    """Tests for GET /api/v1/domains/"""

    def test_list_domains_authenticated(self, authenticated_client, domains):
        """Test listing domains as authenticated user."""
        response = authenticated_client.get('/api/v1/domains/')
        assert response.status_code == 200
        assert isinstance(response.data, list)
        assert len(response.data) == 3

        # Check response structure
        domain = response.data[0]
        assert 'domain_id' in domain
        assert 'name' in domain
        assert 'description' in domain
        assert 'created_at' in domain

    def test_list_domains_unauthenticated(self, api_client):
        """Test listing domains requires authentication."""
        response = api_client.get('/api/v1/domains/')
        assert response.status_code == 401

    def test_list_all_9_domains(self, authenticated_client, db):
        """Test listing returns all 9 fixed domains when initialized."""
        # Create all 9 domains
        domains_data = [
            {'domain_name': 'Culture', 'description': 'Culture'},
            {'domain_name': 'Sport', 'description': 'Sport'},
            {'domain_name': 'Environnement', 'description': 'Environment'},
            {'domain_name': 'Transports', 'description': 'Transport'},
            {'domain_name': 'Sécurité', 'description': 'Security'},
            {'domain_name': 'Santé', 'description': 'Health'},
            {'domain_name': 'Emploi', 'description': 'Employment'},
            {'domain_name': 'Éducation', 'description': 'Education'},
            {'domain_name': 'Numérique', 'description': 'Digital'},
        ]
        for data in domains_data:
            Domain.objects.create(**data)

        response = authenticated_client.get('/api/v1/domains/')
        assert response.status_code == 200
        assert len(response.data) == 9

        # Check all domain names are present
        domain_names = [d['name'] for d in response.data]
        assert 'Culture' in domain_names
        assert 'Sport' in domain_names
        assert 'Environnement' in domain_names
        assert 'Numérique' in domain_names

    def test_list_domains_sorted_by_name(self, authenticated_client, db):
        """Test domains are returned sorted by name."""
        # Create domains out of order
        Domain.objects.create(domain_name='Zeta', description='Z')
        Domain.objects.create(domain_name='Alpha', description='A')
        Domain.objects.create(domain_name='Beta', description='B')

        response = authenticated_client.get('/api/v1/domains/')
        assert response.status_code == 200

        names = [d['name'] for d in response.data]
        assert names == ['Alpha', 'Beta', 'Zeta']

    def test_list_domains_banned_user(self, api_client, test_user):
        """Test banned user cannot list domains."""
        test_user.is_banned = True
        test_user.save()

        client = APIClient()
        client.force_authenticate(user=test_user)

        response = client.get('/api/v1/domains/')
        assert response.status_code == 403


@pytest.mark.django_db
class TestDomainDetailAPI:
    """Tests for GET /api/v1/domains/{id}/"""

    def test_get_domain_detail_success(self, authenticated_client, domains):
        """Test getting domain details successfully."""
        domain = domains[0]
        response = authenticated_client.get(f'/api/v1/domains/{domain.domain_id}/')

        assert response.status_code == 200
        assert response.data['domain_id'] == str(domain.domain_id)
        assert response.data['name'] == domain.domain_name
        assert response.data['description'] == domain.description
        assert 'created_at' in response.data

    def test_get_domain_detail_not_found(self, authenticated_client):
        """Test getting non-existent domain returns 404."""
        fake_id = str(uuid.uuid4())
        response = authenticated_client.get(f'/api/v1/domains/{fake_id}/')

        assert response.status_code == 404
        assert 'error' in response.data
        assert response.data['error']['code'] == 'NOT_FOUND'

    def test_get_domain_detail_unauthenticated(self, api_client, domains):
        """Test getting domain details requires authentication."""
        domain = domains[0]
        response = api_client.get(f'/api/v1/domains/{domain.domain_id}/')
        assert response.status_code == 401

    def test_get_domain_detail_banned_user(self, api_client, test_user, domains):
        """Test banned user cannot get domain details."""
        test_user.is_banned = True
        test_user.save()

        client = APIClient()
        client.force_authenticate(user=test_user)

        domain = domains[0]
        response = client.get(f'/api/v1/domains/{domain.domain_id}/')
        assert response.status_code == 403


@pytest.mark.django_db
class TestDomainSubforumsAPI:
    """Tests for GET /api/v1/domains/{id}/subforums/"""

    def test_get_domain_subforums_empty(self, authenticated_client, domains):
        """Test getting subforums for domain with no subforums."""
        domain = domains[0]
        response = authenticated_client.get(f'/api/v1/domains/{domain.domain_id}/subforums/')

        assert response.status_code == 200
        assert isinstance(response.data, list)
        assert len(response.data) == 0

    def test_get_domain_subforums_with_data(self, authenticated_client, test_user, domains):
        """Test getting subforums for domain with subforums."""
        from db.repositories.domain_repository import SubforumRepository

        domain = domains[0]

        # Create some subforums in the domain
        subforum1 = SubforumRepository.create(
            creator_id=str(test_user.user_id),
            subforum_name='Subforum 1',
            description='Description 1',
            parent_domain_id=str(domain.domain_id)
        )
        subforum2 = SubforumRepository.create(
            creator_id=str(test_user.user_id),
            subforum_name='Subforum 2',
            description='Description 2',
            parent_domain_id=str(domain.domain_id)
        )

        response = authenticated_client.get(f'/api/v1/domains/{domain.domain_id}/subforums/')

        assert response.status_code == 200
        assert len(response.data) == 2

        # Check response structure
        subforum_data = response.data[0]
        assert 'subforum_id' in subforum_data
        assert 'name' in subforum_data
        assert 'description' in subforum_data
        assert 'parent_domain_id' in subforum_data
        assert 'created_at' in subforum_data

    def test_get_domain_subforums_pagination(self, authenticated_client, test_user, domains):
        """Test pagination works for domain subforums."""
        from db.repositories.domain_repository import SubforumRepository

        domain = domains[0]

        # Create 5 subforums
        for i in range(5):
            SubforumRepository.create(
                creator_id=str(test_user.user_id),
                subforum_name=f'Subforum {i}',
                description=f'Description {i}',
                parent_domain_id=str(domain.domain_id)
            )

        # Request page 1 with size 2
        response = authenticated_client.get(
            f'/api/v1/domains/{domain.domain_id}/subforums/?page=1&page_size=2'
        )
        assert response.status_code == 200
        assert len(response.data) == 2

        # Request page 2 with size 2
        response = authenticated_client.get(
            f'/api/v1/domains/{domain.domain_id}/subforums/?page=2&page_size=2'
        )
        assert response.status_code == 200
        assert len(response.data) == 2

    def test_get_domain_subforums_default_pagination(self, authenticated_client, domains):
        """Test default pagination parameters."""
        domain = domains[0]
        response = authenticated_client.get(f'/api/v1/domains/{domain.domain_id}/subforums/')

        assert response.status_code == 200
        # Default should work without errors

    def test_get_domain_subforums_not_found(self, authenticated_client):
        """Test getting subforums for non-existent domain returns error."""
        fake_id = str(uuid.uuid4())
        response = authenticated_client.get(f'/api/v1/domains/{fake_id}/subforums/')

        # Domain service checks if domain exists, should return error
        assert response.status_code in [404, 500]


@pytest.mark.django_db
class TestCreateDomainSubforumAPI:
    """Tests for POST /api/v1/domains/{id}/subforums/create/"""

    def test_create_subforum_success(self, authenticated_client, domains):
        """Test creating a subforum in a domain successfully."""
        domain = domains[0]

        payload = {
            'name': 'New Subforum',
            'description': 'A new subforum for testing'
        }

        response = authenticated_client.post(
            f'/api/v1/domains/{domain.domain_id}/subforums/create/',
            payload,
            format='json'
        )

        assert response.status_code == 201
        assert 'subforum_id' in response.data
        assert response.data['name'] == 'New Subforum'
        assert response.data['description'] == 'A new subforum for testing'
        assert response.data['parent_domain_id'] == str(domain.domain_id)

        # Verify subforum was created in database
        subforum_id = response.data['subforum_id']
        subforum = Subforum.objects.get(subforum_id=subforum_id)
        assert subforum.subforum_name == 'New Subforum'
        assert subforum.parent_domain_id == domain.domain_id

    def test_create_subforum_increments_domain_count(self, authenticated_client, domains):
        """Test creating subforum increments domain subforum count."""
        domain = domains[0]
        initial_count = domain.subforum_count

        payload = {
            'name': 'Test Subforum',
            'description': 'Test'
        }

        response = authenticated_client.post(
            f'/api/v1/domains/{domain.domain_id}/subforums/create/',
            payload,
            format='json'
        )

        assert response.status_code == 201

        # Refresh domain from database
        domain.refresh_from_db()
        assert domain.subforum_count == initial_count + 1

    def test_create_subforum_validation_error_short_name(self, authenticated_client, domains):
        """Test creating subforum with too short name fails."""
        domain = domains[0]

        payload = {
            'name': 'AB',  # Too short (min 3 chars)
            'description': 'Test'
        }

        response = authenticated_client.post(
            f'/api/v1/domains/{domain.domain_id}/subforums/create/',
            payload,
            format='json'
        )

        assert response.status_code == 400

    def test_create_subforum_validation_error_missing_name(self, authenticated_client, domains):
        """Test creating subforum without name fails."""
        domain = domains[0]

        payload = {
            'description': 'Test without name'
        }

        response = authenticated_client.post(
            f'/api/v1/domains/{domain.domain_id}/subforums/create/',
            payload,
            format='json'
        )

        assert response.status_code == 400

    def test_create_subforum_domain_not_found(self, authenticated_client):
        """Test creating subforum in non-existent domain fails."""
        fake_id = str(uuid.uuid4())

        payload = {
            'name': 'Test Subforum',
            'description': 'Test'
        }

        response = authenticated_client.post(
            f'/api/v1/domains/{fake_id}/subforums/create/',
            payload,
            format='json'
        )

        assert response.status_code == 400

    def test_create_subforum_unauthenticated(self, api_client, domains):
        """Test creating subforum requires authentication."""
        domain = domains[0]

        payload = {
            'name': 'Test Subforum',
            'description': 'Test'
        }

        response = api_client.post(
            f'/api/v1/domains/{domain.domain_id}/subforums/create/',
            payload,
            format='json'
        )

        assert response.status_code == 401

    def test_create_subforum_banned_user(self, api_client, test_user, domains):
        """Test banned user cannot create subforum."""
        test_user.is_banned = True
        test_user.save()

        client = APIClient()
        client.force_authenticate(user=test_user)

        domain = domains[0]
        payload = {
            'name': 'Test Subforum',
            'description': 'Test'
        }

        response = client.post(
            f'/api/v1/domains/{domain.domain_id}/subforums/create/',
            payload,
            format='json'
        )

        assert response.status_code == 403

    def test_create_subforum_creates_audit_log(self, authenticated_client, test_user, domains):
        """Test creating subforum creates audit log entry."""
        from db.entities.message_entity import AuditLog

        domain = domains[0]

        payload = {
            'name': 'Audited Subforum',
            'description': 'Test audit'
        }

        initial_log_count = AuditLog.objects.count()

        response = authenticated_client.post(
            f'/api/v1/domains/{domain.domain_id}/subforums/create/',
            payload,
            format='json'
        )

        assert response.status_code == 201

        # Check audit log was created
        assert AuditLog.objects.count() == initial_log_count + 1

        # Verify audit log content
        log = AuditLog.objects.latest('created_at')
        assert log.user_id == test_user.user_id
        assert log.action_type == 'subforum_created'
        assert log.resource_type == 'subforum'
        assert log.resource_id == response.data['subforum_id']


@pytest.mark.django_db
class TestDomainPermissions:
    """Tests for domain-related permissions and access control."""

    def test_regular_user_can_list_domains(self, authenticated_client, domains):
        """Test regular users can list domains."""
        response = authenticated_client.get('/api/v1/domains/')
        assert response.status_code == 200

    def test_regular_user_can_view_domain(self, authenticated_client, domains):
        """Test regular users can view domain details."""
        domain = domains[0]
        response = authenticated_client.get(f'/api/v1/domains/{domain.domain_id}/')
        assert response.status_code == 200

    def test_regular_user_can_create_subforum(self, authenticated_client, domains):
        """Test regular users can create subforums in domains."""
        domain = domains[0]

        payload = {
            'name': 'User Created Subforum',
            'description': 'Created by regular user'
        }

        response = authenticated_client.post(
            f'/api/v1/domains/{domain.domain_id}/subforums/create/',
            payload,
            format='json'
        )

        assert response.status_code == 201

    def test_banned_user_cannot_access_any_domain_endpoint(self, api_client, test_user, domains):
        """Test banned users are blocked from all domain endpoints."""
        test_user.is_banned = True
        test_user.save()

        client = APIClient()
        client.force_authenticate(user=test_user)

        domain = domains[0]

        # List domains
        response = client.get('/api/v1/domains/')
        assert response.status_code == 403

        # Get domain detail
        response = client.get(f'/api/v1/domains/{domain.domain_id}/')
        assert response.status_code == 403

        # Get subforums
        response = client.get(f'/api/v1/domains/{domain.domain_id}/subforums/')
        assert response.status_code == 403

        # Create subforum
        response = client.post(
            f'/api/v1/domains/{domain.domain_id}/subforums/create/',
            {'name': 'Test', 'description': 'Test'},
            format='json'
        )
        assert response.status_code == 403
