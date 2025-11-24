"""
Service for tag management and assignment to posts/forums.
"""
from typing import List, Optional
from django.db import transaction
from db.repositories.tag_repository import TagRepository, PostTagRepository
from db.repositories.post_repository import PostRepository
from db.repositories.user_repository import UserRepository
from db.repositories.message_repository import AuditLogRepository
from db.entities.post_entity import Tag
from common.exceptions import NotFoundError, ValidationError, ConflictError
from common.validators import Validator


class TagService:
    """Service for tags."""

    @staticmethod
    def get_all_tags(page: int = 1, page_size: int = 100) -> List[Tag]:
        return TagRepository.get_all(page, page_size)

    @staticmethod
    @transaction.atomic
    def create_tag(user_id: str, tag_name: str) -> Tag:
        # Validate name
        tag_name = Validator.validate_tag_name(tag_name)

        # Check uniqueness
        existing = TagRepository.get_by_name(tag_name)
        if existing:
            raise ConflictError("Tag already exists")

        tag = TagRepository.create(tag_name=tag_name, creator_id=user_id)

        # Audit
        AuditLogRepository.create(
            user_id=user_id,
            action_type='tag_created',
            resource_type='tag',
            resource_id=str(tag.tag_id)
        )

        return tag

    @staticmethod
    @transaction.atomic
    def assign_tags_to_post(user_id: str, post_id: str, tag_ids: List[str]) -> None:
        # Validate
        post = PostRepository.get_by_id(post_id)
        if not post:
            raise NotFoundError(f"Post {post_id} not found")

        # Only author can assign
        if not post.user or str(post.user.user_id) != user_id:
            raise ValidationError("Only the author can assign tags to the post")

        # Max 5 tags per post
        existing_tags = PostTagRepository.get_by_post(post_id)
        existing_count = len(list(existing_tags))
        if existing_count + len(tag_ids) > 5:
            raise ValidationError("A post cannot have more than 5 tags")

        # Create link for each tag
        for tid in tag_ids:
            tag = TagRepository.get_by_id(tid)
            if not tag:
                raise NotFoundError(f"Tag {tid} not found")
            if PostTagRepository.exists(post_id, tid):
                continue
            PostTagRepository.create(post_id, tid)

        AuditLogRepository.create(
            user_id=user_id,
            action_type='tags_assigned',
            resource_type='post',
            resource_id=post_id,
            details={'tags': tag_ids}
        )

    @staticmethod
    @transaction.atomic
    def unassign_tags_from_post(user_id: str, post_id: str, tag_ids: Optional[List[str]] = None) -> None:
        post = PostRepository.get_by_id(post_id)
        if not post:
            raise NotFoundError(f"Post {post_id} not found")

        # Only author can unassign
        if not post.user or str(post.user.user_id) != user_id:
            raise ValidationError("Only the author can unassign tags from the post")

        if tag_ids is None:
            # remove all
            tags = PostTagRepository.get_by_post(post_id)
            tag_ids = [str(t.tag.tag_id) for t in tags]

        for tid in tag_ids:
            PostTagRepository.delete(post_id, tid)

        AuditLogRepository.create(
            user_id=user_id,
            action_type='tags_unassigned',
            resource_type='post',
            resource_id=post_id,
            details={'tags': tag_ids}
        )
