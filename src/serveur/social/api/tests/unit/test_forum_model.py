import pytest
from django.core.exceptions import ValidationError

from db.entities.domain_entity import Forum
from db.entities.user_entity import User


@pytest.mark.django_db
def test_forum_name_alias_and_defaults():
    user = User.objects.create(firebase_uid='g-test', email='u-test@example.com', username='u_test')
    f = Forum.objects.create(creator=user, forum_name='MyForum', description='A forum')

    # alias returns the same value
    assert f.name == f.forum_name == 'MyForum'

    # defaults
    assert f.member_count == 0
    assert f.post_count == 0
    assert f.forum_id is not None
    assert f.created_at is not None


def test_forum_name_min_length_validation():
    # Validators are executed via full_clean()
    f = Forum(creator=None, forum_name='ab', description='short')
    with pytest.raises(ValidationError):
        f.full_clean()
