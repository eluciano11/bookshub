from rest_framework import permissions


class BookPermission(permissions.BasePermission):
    def is_authenticated(self, request):
        return request.user and request.user.is_authenticated()

    def has_permission(self, request, view, obj=None):
        """
        Returns `True` if the user is authenticated. If the user is
        not authenticated and view.action is `list` or is not safe.
        """
        is_authenticated = self.is_authenticated(request)
        is_safe = request.method in permissions.SAFE_METHODS

        return is_authenticated\
            and is_safe\
            and (obj is None or obj.owner == request.user)
