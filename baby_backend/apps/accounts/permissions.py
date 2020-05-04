from rest_framework import permissions


class IsHaveBillingProfile(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(
            hasattr(request.user, 'billing_profile') or
            request.user.is_staff or
            request.user.is_superuser
        )


class IsReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS or
            request.user.is_superuser
        )


class IsStaffUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.user.is_staff or
            request.user.is_superuser
        )


class IsStaffReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.user.is_staff and request.method in permissions.SAFE_METHODS or
            request.user.is_superuser
        )


class IsStaffOrVendorReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(
            hasattr(request.user, 'vendor') and request.method in permissions.SAFE_METHODS or
            request.user.is_staff or
            request.user.is_superuser
        )


class IsStaffOrVendor(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(
            hasattr(request.user, 'vendor') or
            request.user.is_staff or
            request.user.is_superuser
        )


class IsStaffReadOnlyOrVendorRestricted(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(
            hasattr(request.user, 'vendor') and request.method in permissions.SAFE_METHODS or
            hasattr(request.user, 'vendor') and request.method == 'PATCH' or
            hasattr(request.user, 'vendor') and request.method == 'PUT' or
            request.user.is_staff and request.method in permissions.SAFE_METHODS or
            request.user.is_superuser
        )


class IsStaffOrGuestReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(
            hasattr(request.user, 'guestvendor') and
            request.method in permissions.SAFE_METHODS or
            request.user.is_staff or
            request.user.is_superuser
        )


class IsStaffReadOnlyOrVendor(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(
            hasattr(request.user, 'vendor') or
            request.user.is_staff and request.method in permissions.SAFE_METHODS or
            request.user.is_superuser
        )


class IsStaffReadOnlyOrCustomer(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(
            hasattr(request.user, 'customer') or
            request.user.is_staff and request.method in permissions.SAFE_METHODS or
            request.user.is_superuser
        )


class IsStaffReadOnlyOrCustomerReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(
            hasattr(request.user, 'customer') and request.method in permissions.SAFE_METHODS or
            request.user.is_staff and request.method in permissions.SAFE_METHODS or
            request.user.is_superuser
        )


class IsStaffReadOnlyOrCustomerRestricted(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(
            hasattr(request.user, 'customer') and request.method in permissions.SAFE_METHODS or
            hasattr(request.user, 'customer') and request.method == 'PATCH' or
            hasattr(request.user, 'customer') and request.method == 'PUT' or
            request.user.is_staff and request.method in permissions.SAFE_METHODS or
            request.user.is_superuser
        )


class IsStaffReadOnlyOrVendorPostOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(
            hasattr(request.user, 'vendor') and request.method in permissions.SAFE_METHODS or
            hasattr(request.user, 'vendor') and request.method == 'POST' or
            request.user.is_staff and request.method in permissions.SAFE_METHODS or
            request.user.is_superuser
        )


class IsStaffReadOnlyOrVendorPatchOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(
            hasattr(request.user, 'vendor') and request.method in permissions.SAFE_METHODS or
            hasattr(request.user, 'vendor') and request.method == 'PATCH' or
            request.user.is_staff and request.method in permissions.SAFE_METHODS or
            request.user.is_superuser
        )


class IsStaffReadOnlyOrVendorReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(
            hasattr(request.user, 'vendor') and request.method in permissions.SAFE_METHODS or
            request.user.is_staff and request.method in permissions.SAFE_METHODS or
            request.user.is_superuser
        )


class IsAssociatedWithUser(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if hasattr(request.user, 'vendor'):
            return bool(
                request.user == obj
            )
        else:
            return bool(
                request.user.is_superuser or
                request.user.is_staff and request.method in permissions.SAFE_METHODS
            )
