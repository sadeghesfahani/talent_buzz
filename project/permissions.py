from rest_framework import permissions

from project.models import GigApplication, ProjectApplication


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the project or gig.
        if isinstance(obj, GigApplication):
            return obj.gig.project.associated_user == request.user
        elif isinstance(obj, ProjectApplication):
            return obj.project.associated_user == request.user
        return False
