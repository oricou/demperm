"""
Custom permissions for API endpoints.
"""
from rest_framework import permissions as rf_permissions
from rest_framework import exceptions as rf_exceptions
from db.repositories.user_repository import BlockRepository


class IsAuthenticated(rf_permissions.IsAuthenticated):
    """Alias of DRF's IsAuthenticated that explicitly raises NotAuthenticated
    to ensure the framework returns HTTP 401 for unauthenticated requests.
    """
    def has_permission(self, request, view):
        is_auth = bool(request.user and getattr(request.user, 'is_authenticated', False))
        if not is_auth:
            raise rf_exceptions.NotAuthenticated()
        return True


class IsAdmin(rf_permissions.BasePermission):
    """
    Allow access only to admin users.
    """
    
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            hasattr(request.user, 'is_admin') and
            request.user.is_admin
        )


class IsOwnerOrAdmin(rf_permissions.BasePermission):
    """
    Allow access only to the owner of the object or admin.
    """
    
    def has_object_permission(self, request, view, obj):
        # Admin can access everything
        if hasattr(request.user, 'is_admin') and request.user.is_admin:
            return True
        
        # Check if user is the owner
        if hasattr(obj, 'user_id'):
            return str(obj.user_id) == str(request.user.user_id)
        elif hasattr(obj, 'user'):
            return str(obj.user.user_id) == str(request.user.user_id)
        
        return False


class IsNotBanned(rf_permissions.BasePermission):
    """
    Deny access to banned users.
    """
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return True  # Let authentication handle this
        
        return not getattr(request.user, 'is_banned', False)


class IsNotBlocked(rf_permissions.BasePermission):
    """
    Check if users have blocked each other.
    """
    
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return True
        
        # Get the target user from the object
        target_user_id = None
        if hasattr(obj, 'user_id'):
            target_user_id = str(obj.user_id)
        elif hasattr(obj, 'user'):
            target_user_id = str(obj.user.user_id)
        
        if not target_user_id:
            return True
        
        current_user_id = str(request.user.user_id)
        
        # Check if either user has blocked the other
        if BlockRepository.is_blocked(current_user_id, target_user_id):
            return False
        if BlockRepository.is_blocked(target_user_id, current_user_id):
            return False
        
        return True


class CanViewProfile(rf_permissions.BasePermission):
    """
    Check if user can view a profile based on privacy settings.
    """
    
    def has_object_permission(self, request, view, obj):
        # Public profiles are visible to everyone (privacy True == public)
        if hasattr(obj, 'profile') and obj.profile.privacy:
            return True
        
        # Owner can always view their own profile
        if request.user and request.user.is_authenticated:
            if str(obj.user_id) == str(request.user.user_id):
                return True
            
            # Admin can view all profiles
            if hasattr(request.user, 'is_admin') and request.user.is_admin:
                return True
            
            # For private profiles, check if requester is a follower
            if hasattr(obj, 'profile') and not obj.profile.privacy:
                from db.repositories.user_repository import FollowRepository
                followers = FollowRepository.get_followers(str(obj.user_id), status='accepted')
                follower_ids = [str(f.follower_id) for f in followers]
                return str(request.user.user_id) in follower_ids
        
        return False


class CanViewPost(rf_permissions.BasePermission):
    """
    Check if user can view a post based on author's privacy settings.
    """
    
    def has_object_permission(self, request, view, obj):
        # Get the post author
        if not hasattr(obj, 'user') or not obj.user:
            return True  # Orphaned post
        
        author = obj.user
        
        # Public profiles - posts visible to all (privacy True == public)
        if hasattr(author, 'profile') and author.profile.privacy:
            return True
        
        # Author can always view their own posts
        if request.user and request.user.is_authenticated:
            if str(author.user_id) == str(request.user.user_id):
                return True
            
            # Admin can view all posts
            if hasattr(request.user, 'is_admin') and request.user.is_admin:
                return True
            
            # For private profiles, check if requester is a follower
            if hasattr(author, 'profile') and not author.profile.privacy:
                from db.repositories.user_repository import FollowRepository
                followers = FollowRepository.get_followers(str(author.user_id), status='accepted')
                follower_ids = [str(f.follower_id) for f in followers]
                return str(request.user.user_id) in follower_ids
        
        return False

