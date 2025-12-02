# tests/unit/test_subforum_model.py
import pytest
from db.entities.domain_entity import Subforum, Domain, Forum
from db.entities.user_entity import User
from django.db import IntegrityError

@pytest.mark.django_db
def test_subforum_must_have_exactly_one_parent():
    # create ORM objects directly instead of relying on factory fixtures
    user = User.objects.create(firebase_uid='g-f', email='u-f@example.com', username='u_forum')
    domain = Domain.objects.create(domain_name='TestDomain', description='d')
    forum = Forum.objects.create(creator=user, forum_name='TestForum', description='d')

    # both parents set -> should violate check constraint / be rejected by DB
    with pytest.raises(IntegrityError):
        Subforum.objects.create(
            creator=user,
            subforum_name="BothParent",
            parent_domain=domain,
            parent_forum=forum
        )


@pytest.mark.django_db
def test_subforum_allows_single_parent_domain_or_forum():
    user = User.objects.create(firebase_uid='g-d', email='u-d@example.com', username='u_domain')
    domain = Domain.objects.create(domain_name='DomainOnly', description='d')
    forum_creator = User.objects.create(firebase_uid='g-fo', email='f-o@example.com', username='forum_owner')
    forum = Forum.objects.create(creator=forum_creator, forum_name='ForumOnly', description='d')

    # parent_domain only should succeed
    s1 = Subforum.objects.create(creator=user, subforum_name='DomainSub', parent_domain=domain)
    assert s1.parent_domain_id == domain.domain_id
    assert s1.parent_forum_id is None

    # parent_forum only should succeed
    s2 = Subforum.objects.create(creator=user, subforum_name='ForumSub', parent_forum=forum)
    assert s2.parent_forum_id == forum.forum_id
    assert s2.parent_domain_id is None
