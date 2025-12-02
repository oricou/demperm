"""
Repositories for Tag and PostTag operations.
"""
from typing import List, Optional
from db.entities.post_entity import Tag, PostTag


class TagRepository:
    """Repository for Tag entity operations."""

    @staticmethod
    def create(tag_name: str, creator_id: Optional[str] = None) -> Tag:
        return Tag.objects.create(tag_name=tag_name, creator_id=creator_id)

    @staticmethod
    def get_by_id(tag_id: str) -> Optional[Tag]:
        try:
            return Tag.objects.get(tag_id=tag_id)
        except Tag.DoesNotExist:
            return None

    @staticmethod
    def get_by_name(tag_name: str) -> Optional[Tag]:
        try:
            return Tag.objects.get(tag_name=tag_name)
        except Tag.DoesNotExist:
            return None

    @staticmethod
    def get_all(page: int = 1, page_size: int = 100) -> List[Tag]:
        offset = (page - 1) * page_size
        return Tag.objects.order_by('tag_name')[offset:offset + page_size]

    @staticmethod
    def delete(tag_id: str) -> bool:
        deleted, _ = Tag.objects.filter(tag_id=tag_id).delete()
        return deleted > 0


class PostTagRepository:
    """Repository for PostTag linking posts and tags."""

    @staticmethod
    def create(post_id: str, tag_id: str) -> PostTag:
        return PostTag.objects.create(post_id=post_id, tag_id=tag_id)

    @staticmethod
    def delete(post_id: str, tag_id: str) -> bool:
        deleted, _ = PostTag.objects.filter(post_id=post_id, tag_id=tag_id).delete()
        return deleted > 0

    @staticmethod
    def exists(post_id: str, tag_id: str) -> bool:
        return PostTag.objects.filter(post_id=post_id, tag_id=tag_id).exists()

    @staticmethod
    def get_by_post(post_id: str) -> List[PostTag]:
        return PostTag.objects.filter(post_id=post_id).select_related('tag')
