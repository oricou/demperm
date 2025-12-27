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
