from rest_framework.permissions import BasePermission


class ProductsPermission(BasePermission):
    """
    Only allows the common user to list and retrive, 
    requires staff status to alter a product.
    """

    def has_permission(self, request, view):

        if view.action in ['list', 'retrieve']:
            return True

        else:
            return request.user.is_staff
