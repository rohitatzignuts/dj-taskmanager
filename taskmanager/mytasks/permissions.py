from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        print(f"Request User: {request.user}") 
        print(f"Object Owner: {obj.added_by}")

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.added_by == request.user
