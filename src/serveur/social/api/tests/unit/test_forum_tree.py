import pytest
from rest_framework.test import APIRequestFactory, force_authenticate

from db.entities.user_entity import User
from db.repositories.domain_repository import ForumRepository, SubforumRepository
from api.apps.forums.views import ForumTreeView


@pytest.mark.django_db
def test_forum_tree_structure():
    # create user and root forum
    user = User.objects.create(firebase_uid='t1', email='t1@example.com', username='tester')
    forum = ForumRepository.create(creator_id=str(user.user_id), forum_name='RootForum', description='root')

    # create a subforum under the forum (this will create a forum for the subforum)
    parent = SubforumRepository.create(
        creator_id=str(user.user_id),
        subforum_name='ParentSub',
        parent_forum_id=str(forum.forum_id)
    )

    # create a nested subforum under the parent (parent.forum_id is the forum representing parent)
    # parent.forum_id is a Forum instance on Subforum; use the raw id attribute
    child = SubforumRepository.create(
        creator_id=str(user.user_id),
        subforum_name='ChildSub',
        parent_forum_id=str(parent.forum_id_id)
    )

    # call the tree view and assert hierarchical structure
    factory = APIRequestFactory()
    request = factory.get(f"/api/v1/forums/{forum.forum_id}/tree/")
    force_authenticate(request, user=user)

    view = ForumTreeView.as_view()
    response = view(request, forum_id=str(forum.forum_id))

    assert response.status_code == 200
    data = response.data

    # root should contain one child (ParentSub), which in turn contains one child (ChildSub)
    assert isinstance(data, list)
    assert len(data) == 1
    root_node = data[0]
    assert root_node['name'] == 'ParentSub'
    assert isinstance(root_node.get('children', []), list)
    assert len(root_node['children']) == 1
    child_node = root_node['children'][0]
    assert child_node['name'] == 'ChildSub'
    assert child_node.get('children') == []
