from rest_framework import permissions


class IsAssociatedWithVendor(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if hasattr(request.user, 'vendor'):
            return bool(
                request.user.vendor == obj
            )
        else:
            return bool(
                request.user.is_superuser or
                request.user.is_staff
            )


class IsAssociatedWithBankAccount(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if hasattr(request.user, 'vendor'):
            return bool(
                request.user.vendor.vendorbankaccount == obj
            )
        else:
            return bool(
                request.user.is_superuser or
                request.user.is_staff
            )


class IsAssociatedWithVendorDeliveryAddress(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if hasattr(request.user, 'vendor'):
            return bool(
                request.user.vendor.vendordeliveryaddress_set.filter(vendor=obj.vendor).exists()
            )
        else:
            return bool(
                request.user.is_superuser or
                request.user.is_staff
            )


class IsAssociatedWithVendorBillingAddress(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if hasattr(request.user, 'vendor'):
            return bool(
                request.user.vendor.vendorbillingaddress_set.filter(vendor=obj.vendor).exists()
            )
        else:
            return bool(
                request.user.is_superuser or
                request.user.is_staff
            )


class IsAssociatedWithInstagram(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if hasattr(request.user, 'vendor'):
            return bool(
                request.user.vendor.vendorinstagram_set.filter(pk=obj.pk).exists()
            )
        else:
            return bool(
                request.user.is_superuser or
                request.user.is_staff
            )


class IsAssociatedWithDiscount(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if hasattr(request.user, 'vendor'):
            return bool(
                request.user.vendor.vendordiscount_set.filter(pk=obj.pk).exists()
            )
        else:
            return bool(
                request.user.is_superuser or
                request.user.is_staff
            )


class IsAssociatedWithBalance(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if hasattr(request.user, 'vendor'):
            return bool(
                request.user.vendor.vendorbalance == obj
            )
        else:
            return bool(
                request.user.is_superuser or
                request.user.is_staff
            )


class IsAssociatedWithVendorCustomer(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if hasattr(request.user, 'vendor'):
            return bool(
                request.user.vendor.vendorcustomer_set.filter(pk=obj.pk).exists()
            )
        else:
            return bool(
                request.user.is_superuser or
                request.user.is_staff
            )
