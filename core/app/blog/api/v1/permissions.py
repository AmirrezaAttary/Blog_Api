from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Only owners can edit a post.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user
