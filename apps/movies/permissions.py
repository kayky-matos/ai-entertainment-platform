from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the object
        return obj.user == request.user


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow administrators to create, edit, or delete objects,
    while allowing read-only access to others.
    """

    def has_permission(self, request, view):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to admin users
        return request.user and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to admin users
        return request.user and request.user.is_staff


class IsModeratorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow moderators to manage content while allowing
    read-only access to others. Moderators are users with is_staff=True
    but not necessarily is_superuser=True.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user and request.user.is_staff


class CanManageContentWarnings(permissions.BasePermission):
    """
    Custom permission to only allow authorized users to manage content warnings.
    This includes both administrators and content moderators.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        # Check if user is admin or has content moderator role
        return (
                request.user and
                (request.user.is_staff or
                 hasattr(request.user, 'profile') and
                 request.user.profile.is_content_moderator)
        )


class CanSubmitReviews(permissions.BasePermission):
    """
    Custom permission to control who can submit reviews.
    Users must be authenticated and have a verified email.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        # Check if user is authenticated and has verified email
        return (
                request.user and
                request.user.is_authenticated and
                hasattr(request.user, 'profile') and
                request.user.profile.is_email_verified
        )


class CanManageStreamingInfo(permissions.BasePermission):
    """
    Custom permission to control who can manage streaming availability information.
    This includes administrators and authorized content managers.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        # Check if user is admin or has streaming manager role
        return (
                request.user and
                (request.user.is_staff or
                 hasattr(request.user, 'profile') and
                 request.user.profile.is_streaming_manager)
        )


class CanManageNews(permissions.BasePermission):
    """
    Custom permission to control who can manage movie news.
    This includes administrators and news editors.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        # Check if user is admin or has news editor role
        return (
                request.user and
                (request.user.is_staff or
                 hasattr(request.user, 'profile') and
                 request.user.profile.is_news_editor)
        )


class HasVerifiedAccount(permissions.BasePermission):
    """
    Custom permission to ensure user has a verified account before
    performing certain actions (like rating movies or writing reviews).
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return (
                request.user and
                request.user.is_authenticated and
                hasattr(request.user, 'profile') and
                request.user.profile.is_verified
        )


class RateLimitedPermission(permissions.BasePermission):
    """
    Custom permission to implement rate limiting for certain actions.
    This can be used to prevent spam in reviews, ratings, etc.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if not request.user or not request.user.is_authenticated:
            return False

        # Implementation would typically check Redis or similar for rate limiting
        from django.core.cache import cache

        user_key = f"rate_limit_{request.user.id}"
        attempt_count = cache.get(user_key, 0)

        # Example: Limit to 10 requests per minute
        if attempt_count >= 10:
            return False

        cache.set(user_key, attempt_count + 1, 60)  # 60 seconds expiration
        return True