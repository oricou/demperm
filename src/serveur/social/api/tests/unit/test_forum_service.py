import pytest
from services.apps_services.forum_service import ForumService
from common.exceptions import ConflictError, NotFoundError


from db.entities.user_entity import User
from db.entities.domain_entity import Forum, Membership
from common.exceptions import PermissionDeniedError


@pytest.mark.django_db
def test_create_forum_auto_joins_and_counts():
    # creator should be auto-joined as moderator and member_count incremented
    user = User.objects.create(firebase_uid='g1', email='c1@example.com', username='creator1')
    forum = ForumService.create_forum(str(user.user_id), 'My Forum', 'desc')

    assert forum.forum_name == 'My Forum'

    # membership exists
    membership = Membership.objects.filter(user_id=user.user_id, forum_id=forum.forum_id).first()
    assert membership is not None
    assert membership.role == 'moderator'

    # member count should be incremented to 1
    f = Forum.objects.get(forum_id=forum.forum_id)
    assert f.member_count == 1


@pytest.mark.django_db
def test_get_forum_by_id_not_found():
    with pytest.raises(NotFoundError):
        ForumService.get_forum_by_id('00000000-0000-0000-0000-000000000000')


@pytest.mark.django_db
def test_join_forum_success_and_conflict():
    creator = User.objects.create(firebase_uid='g2', email='c2@example.com', username='creator2')
    forum = ForumService.create_forum(str(creator.user_id), 'Joinable Forum', 'd')

    user = User.objects.create(firebase_uid='g3', email='u3@example.com', username='user3')

    # user joins successfully
    membership = ForumService.join_forum(str(user.user_id), str(forum.forum_id))
    assert str(membership.user_id) == str(user.user_id)
    assert str(membership.forum_id) == str(forum.forum_id)

    # joining again raises ConflictError
    with pytest.raises(ConflictError):
        ForumService.join_forum(str(user.user_id), str(forum.forum_id))


@pytest.mark.django_db
def test_leave_forum_not_member_and_creator_cannot_leave():
    creator = User.objects.create(firebase_uid='g4', email='c4@example.com', username='creator4')
    forum = ForumService.create_forum(str(creator.user_id), 'LeaveForum', 'd')

    other = User.objects.create(firebase_uid='g5', email='o5@example.com', username='other5')

    # other trying to leave (not a member) should raise NotFoundError
    with pytest.raises(NotFoundError):
        ForumService.leave_forum(str(other.user_id), str(forum.forum_id))

    # creator cannot leave
    with pytest.raises(PermissionDeniedError):
        ForumService.leave_forum(str(creator.user_id), str(forum.forum_id))


@pytest.mark.django_db
def test_join_forum_conflict():
    user = User.objects.create(firebase_uid='g6', email='c6@example.com', username='conflict_user')
    creator = User.objects.create(firebase_uid='g7', email='f7@example.com', username='forum_owner')
    forum = ForumService.create_forum(str(creator.user_id), 'ConflictForum', 'd')

    # first join succeeds
    ForumService.join_forum(str(user.user_id), str(forum.forum_id))

    # second join must raise ConflictError
    with pytest.raises(ConflictError):
        ForumService.join_forum(str(user.user_id), str(forum.forum_id))
