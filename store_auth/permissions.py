from rest_framework.permissions import BasePermission


class UserPermission(BaseException):
    """
    Allows creation of new users, but requires the actual
    user to make alterations to its data.
    """

    def has_permission(self, request, view):

        user = request.user
        if view.action == 'create':
            return not user.is_authenticated

        elif view.action in ['update', 'partial_update', 'destroy']:
            return user.is_authenticated

        else:
            return False

    def has_object_permission(self, request, view, obj):
        return request.user == obj
