import pytest
from db.entities.post_entity import Post


@pytest.mark.django_db
def test_forum_subforums_create_and_list(authenticated_client):
    client = authenticated_client

    # create a forum
    r = client.post('/api/v1/forums/create/', {'name': 'Forum With Subs', 'description': 'FWS'}, format='json')
    assert r.status_code == 201
    forum_id = r.data['forum_id']

    # create subforum under forum
    payload = {'name': 'Sub A', 'description': 'Subforum A'}
    r = client.post(f'/api/v1/forums/{forum_id}/subforums/create/', payload, format='json')
    assert r.status_code == 201
    sub_id = r.data['subforum_id']

    # list forum subforums
    r = client.get(f'/api/v1/forums/{forum_id}/subforums/')
    assert r.status_code == 200
    assert any(s.get('subforum_id') == sub_id for s in r.data)


@pytest.mark.django_db
def test_domain_subforums_create_and_list(authenticated_client, domains):
    client = authenticated_client
    domain = domains[0]

    # create subforum under domain
    payload = {'name': 'Domain Sub', 'description': 'Domain level subforum'}
    r = client.post(f'/api/v1/domains/{domain.domain_id}/subforums/create/', payload, format='json')
    assert r.status_code == 201
    sub_id = r.data['subforum_id']

    # list domain subforums
    r = client.get(f'/api/v1/domains/{domain.domain_id}/subforums/')
    assert r.status_code == 200
    assert any(s.get('subforum_id') == sub_id for s in r.data)


@pytest.mark.django_db
def test_subforum_detail_and_posts(authenticated_client, test_user):
    client = authenticated_client

    # create a forum & subforum via API
    r = client.post('/api/v1/forums/create/', {'name': 'Forum Posts', 'description': 'FP'}, format='json')
    assert r.status_code == 201
    forum_id = r.data['forum_id']
    r = client.post(f'/api/v1/forums/{forum_id}/subforums/create/', {'name': 'Posts Sub', 'description': 'PS'}, format='json')
    assert r.status_code == 201
    sub_id = r.data['subforum_id']

    # create a post in the subforum using ORM (simpler than full post create flow)
    post = Post.objects.create(user=test_user, subforum_id=sub_id, title='T', content='C')

    # get subforum detail
    r = client.get(f'/api/v1/subforums/{sub_id}/')
    assert r.status_code == 200
    assert r.data['subforum_id'] == sub_id

    # get posts in subforum
    r = client.get(f'/api/v1/subforums/{sub_id}/posts/')
    assert r.status_code == 200
    assert any(p.get('post_id') == str(post.post_id) for p in r.data)


@pytest.mark.django_db
def test_subforum_subscribe_unsubscribe(authenticated_client):
    client = authenticated_client

    # create forum and subforum
    r = client.post('/api/v1/forums/create/', {'name': 'SubSubTest', 'description': 'SST'}, format='json')
    assert r.status_code == 201
    forum_id = r.data['forum_id']
    r = client.post(f'/api/v1/forums/{forum_id}/subforums/create/', {'name': 'ToSubscribe', 'description': 'Subscribe desc'}, format='json')
    assert r.status_code == 201
    sub_id = r.data['subforum_id']

    # subscribe
    r = client.post(f'/api/v1/subscriptions/subforums/{sub_id}/')
    assert r.status_code == 201

    # unsubscribe
    r = client.delete(f'/api/v1/subscriptions/subforums/{sub_id}/unsubscribe/')
    assert r.status_code == 204


@pytest.mark.django_db
def test_subforum_detail_not_found(monkeypatch, authenticated_client):
    from common.exceptions import NotFoundError

    def _raise(*args, **kwargs):
        raise NotFoundError('no subforum')

    monkeypatch.setattr('services.apps_services.domain_service.DomainService.get_subforum_by_id', _raise)

    import uuid
    sid = str(uuid.uuid4())
    resp = authenticated_client.get(f'/api/v1/subforums/{sid}/')
    assert resp.status_code == 404
    assert resp.json().get('error', {}).get('code') == 'NOT_FOUND'


@pytest.mark.django_db
def test_subforum_posts_not_found(monkeypatch, authenticated_client):
    from common.exceptions import NotFoundError

    def _raise(*args, **kwargs):
        raise NotFoundError('no subforum')

    monkeypatch.setattr('services.apps_services.domain_service.DomainService.get_subforum_by_id', _raise)

    import uuid
    sid = str(uuid.uuid4())
    resp = authenticated_client.get(f'/api/v1/subforums/{sid}/posts/')
    assert resp.status_code == 404
    assert resp.json().get('error', {}).get('code') == 'NOT_FOUND'


@pytest.mark.django_db
def test_create_forum_subforum_validation_error(monkeypatch, authenticated_client):
    from common.exceptions import ValidationError
    # create a forum first
    r = authenticated_client.post('/api/v1/forums/create/', {'name': 'ValidForum', 'description': 'desc'}, format='json')
    assert r.status_code == 201
    forum_id = r.data['forum_id']

    def _raise(*args, **kwargs):
        raise ValidationError('bad name')

    monkeypatch.setattr('common.validators.Validator.validate_forum_name', _raise)

    resp = authenticated_client.post(f'/api/v1/forums/{forum_id}/subforums/create/', data={'name': 'x', 'description': 'd'}, format='json')
    assert resp.status_code == 400
    assert resp.json().get('error', {}).get('code') == 'VALIDATION_ERROR'

