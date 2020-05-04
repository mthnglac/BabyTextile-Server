from rest_framework import permissions


class IsAssociatedWithGuest(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if hasattr(request.user, 'guestvendor'):
            return bool(
                request.user.guestvendor == obj
            )
        else:
            return bool(
                request.user.is_superuser or
                request.user.is_staff
            )
