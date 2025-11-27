"""
Expose all database models for Django migrations.
"""
from db.entities.user_entity import User, UserProfile, UserSettings, Block, Follow
from db.entities.domain_entity import Domain, Forum, Subforum, Membership
from db.entities.post_entity import Post, Comment, Like, Tag, PostTag, ForumTag
from db.entities.message_entity import Message, Report, AuditLog

__all__ = [
    'User',
    'UserProfile',
    'UserSettings',
    'Block',
    'Follow',
    'Domain',
    'Forum',
    'Subforum',
    'Membership',
    'Post',
    'Comment',
    'Like',
    'Tag',
    'PostTag',
    'ForumTag',
    'Message',
    'Report',
    'AuditLog',
]

