import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_create_list_and_get_forum(authenticated_client):
    client = authenticated_client

    # initially list forums (may be empty)
    r = client.get('/api/v1/forums/')
    assert r.status_code == 200

    # create a forum
    payload = {'name': 'Test Forum', 'description': 'A forum for testing'}
    r = client.post('/api/v1/forums/create/', payload, format='json')
    assert r.status_code == 201
    forum_id = r.data['forum_id']

    # get detail
    r = client.get(f'/api/v1/forums/{forum_id}/')
    assert r.status_code == 200
    assert r.data['name'] == 'Test Forum'


@pytest.mark.django_db
def test_forums_me_and_search(authenticated_client, test_user):
    client = authenticated_client

    # create two forums
    r1 = client.post('/api/v1/forums/create/', {'name': 'Alpha Forum', 'description': 'A'}, format='json')
    r2 = client.post('/api/v1/forums/create/', {'name': 'Beta Forum', 'description': 'B'}, format='json')
    assert r1.status_code == 201 and r2.status_code == 201

    forum_id = r1.data['forum_id']

    # subscribe to forum via subscriptions endpoint
    r = client.post(f'/api/v1/subscriptions/forums/{forum_id}/')
    # If the authenticated user created the forum they are already a member;
    # accept either success or conflict (already member).
    assert r.status_code in (201, 400)

    # GET /forums/me should list subscribed forums
    r = client.get('/api/v1/forums/me/')
    assert r.status_code == 200
    names = [f['name'] for f in r.data]
    assert 'Alpha Forum' in names

    # search forums
    r = client.get('/api/v1/forums/search/?query=Alpha')
    assert r.status_code == 200
    assert any('Alpha Forum' == f.get('name') for f in r.data)


@pytest.mark.django_db
def test_join_and_leave_forum(authenticated_client, admin_client):
    # Create a forum as admin, then join/leave with authenticated_client
    aclient = admin_client
    client = authenticated_client

    # admin creates a forum
    r = aclient.post('/api/v1/forums/create/', {'name': 'JoinLeaveForum', 'description': 'JL'}, format='json')
    assert r.status_code == 201
    forum_id = r.data['forum_id']

    # join via forums join endpoint (as authenticated_client)
    r = client.post(f'/api/v1/forums/{forum_id}/join/')
    assert r.status_code == 201

    # joining again should return an error (conflict)
    r = client.post(f'/api/v1/forums/{forum_id}/join/')
    assert r.status_code == 400

    # leave forum
    r = client.delete(f'/api/v1/forums/{forum_id}/leave/')
    assert r.status_code == 204


@pytest.mark.django_db
def test_forums_pagination(authenticated_client):
    client = authenticated_client

    # create three forums
    for i in range(3):
        r = client.post('/api/v1/forums/create/', {'name': f'Pg{i}', 'description': 'P'}, format='json')
        assert r.status_code == 201

    # request page size 2
    r = client.get('/api/v1/forums/?page=1&page_size=2')
    assert r.status_code == 200
    assert len(r.data) <= 2


@pytest.mark.django_db
def test_create_forum_validation(authenticated_client):
    client = authenticated_client

    # missing name should return validation error
    r = client.post('/api/v1/forums/create/', {'description': 'No name'}, format='json')
    assert r.status_code == 400


@pytest.mark.django_db
def test_search_requires_query(authenticated_client):
    client = authenticated_client

    r = client.get('/api/v1/forums/search/')
    assert r.status_code == 400
    assert 'VALIDATION_ERROR' in str(r.data.get('error', {}))


@pytest.mark.django_db
def test_forum_subforums_create_and_list_via_forums(authenticated_client):
    client = authenticated_client

    # create a forum
    r = client.post('/api/v1/forums/create/', {'name': 'Forum SubTest', 'description': 'FS'}, format='json')
    assert r.status_code == 201
    forum_id = r.data['forum_id']

    # create a subforum under forum via forums endpoint
    r = client.post(f'/api/v1/forums/{forum_id}/subforums/create/', {'name': 'ChildSub', 'description': 'CS'}, format='json')
    assert r.status_code == 201
    sub_id = r.data['subforum_id']

    # list subforums under forum
    r = client.get(f'/api/v1/forums/{forum_id}/subforums/')
    assert r.status_code == 200
    assert any(s.get('subforum_id') == sub_id for s in r.data)


@pytest.mark.django_db
def test_create_forum_validation_error(monkeypatch, authenticated_client):
    from common.exceptions import ValidationError

    def _raise(*args, **kwargs):
        raise ValidationError("Invalid forum")

    monkeypatch.setattr('services.apps_services.forum_service.ForumService.create_forum', _raise)

    resp = authenticated_client.post('/api/v1/forums/create/', data={'name': 'x', 'description': 'd'}, format='json')
    assert resp.status_code == 400
    assert resp.json().get('error', {}).get('code') == 'VALIDATION_ERROR'


@pytest.mark.django_db
def test_forum_detail_not_found(monkeypatch, authenticated_client):
    from common.exceptions import NotFoundError

    def _raise(*args, **kwargs):
        raise NotFoundError('not found')

    monkeypatch.setattr('services.apps_services.forum_service.ForumService.get_forum_by_id', _raise)

    import uuid
    fid = str(uuid.uuid4())
    resp = authenticated_client.get(f'/api/v1/forums/{fid}/')
    assert resp.status_code == 404
    assert resp.json().get('error', {}).get('code') == 'NOT_FOUND'


@pytest.mark.django_db
def test_leave_forum_not_found(monkeypatch, authenticated_client):
    from common.exceptions import NotFoundError

    def _raise(*args, **kwargs):
        raise NotFoundError('not a member')

    monkeypatch.setattr('services.apps_services.forum_service.ForumService.leave_forum', _raise)

    import uuid
    fid = str(uuid.uuid4())
    resp = authenticated_client.delete(f'/api/v1/forums/{fid}/leave/')
    assert resp.status_code == 404
    assert resp.json().get('error', {}).get('code') == 'NOT_FOUND'


@pytest.mark.django_db
def test_join_forum_conflict(monkeypatch, authenticated_client):
    from common.exceptions import ConflictError

    def _raise(*args, **kwargs):
        raise ConflictError('already member')

    monkeypatch.setattr('services.apps_services.forum_service.ForumService.join_forum', _raise)

    import uuid
    fid = str(uuid.uuid4())
    resp = authenticated_client.post(f'/api/v1/forums/{fid}/join/')
    assert resp.status_code == 400
    assert resp.json().get('error', {}).get('code') == 'ERROR'


@pytest.mark.django_db
def test_forum_subforums_forum_not_found_integration(monkeypatch, authenticated_client):
    from common.exceptions import NotFoundError

    def _raise(*args, **kwargs):
        raise NotFoundError('forum missing')

    monkeypatch.setattr('services.apps_services.forum_service.ForumService.get_forum_by_id', _raise)

    import uuid
    fid = str(uuid.uuid4())
    resp = authenticated_client.get(f'/api/v1/forums/{fid}/subforums/')
    assert resp.status_code == 404
    assert resp.json().get('error', {}).get('code') == 'NOT_FOUND'


@pytest.mark.django_db
def test_leave_forum_permission_denied(monkeypatch, authenticated_client):
    from common.exceptions import PermissionDeniedError

    def _raise(*args, **kwargs):
        raise PermissionDeniedError('Forum creator cannot leave the forum')

    monkeypatch.setattr('services.apps_services.forum_service.ForumService.leave_forum', _raise)

    import uuid
    fid = str(uuid.uuid4())
    resp = authenticated_client.delete(f'/api/v1/forums/{fid}/leave/')
    assert resp.status_code == 403
    assert resp.json().get('error', {}).get('code') == 'PERMISSION_DENIED'

