from rest_framework import permissions


class BookPermission(permissions.BasePermission):
    def is_authenticated(self, request):
        return request.user and request.user.is_authenticated()

    def has_permission(self, request, view, obj=None):
        """
        Returns `True` if the user is authenticated
        and is owner of the object.
        """
        is_authenticated = self.is_authenticated(request)

        return is_authenticated\
            and (obj is None or obj.owner == request.user)
