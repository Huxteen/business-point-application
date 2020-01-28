from rest_framework import permissions


class PostPermission(permissions.BasePermission):
    """Allows users to edit their own post."""

    def has_object_permission(self, request, view, obj):
        """Check user is trying to edit their own post."""

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user_id_id == request.user.id


    def has_permission(self, request, view):
        if view.action == 'list':
            return True
        elif view.action == 'create':
           return request.user.is_authenticated
        elif view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return True
        else:
            return False
