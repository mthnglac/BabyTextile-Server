from rest_framework import permissions


class IsAssociatedWithCustomer(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if hasattr(request.user, 'customer'):
            return bool(
                request.user.customer == obj
            )
        else:
            return bool(
                request.user.is_superuser or
                request.user.is_staff and request.method in permissions.SAFE_METHODS
            )


class IsAssociatedWithCustomerDeliveryAddress(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if hasattr(request.user, 'customer'):
            return bool(
                request.user.customer.customerdeliveryaddress_set.filter(pk=obj.pk).exists()
            )
        else:
            return bool(
                request.user.is_superuser or
                request.user.is_staff and request.method in permissions.SAFE_METHODS
            )


class IsAssociatedWithCustomerBillingAddress(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if hasattr(request.user, 'customer'):
            return bool(
                request.user.customer.customerbillingaddress_set.filter(pk=obj.pk).exists()
            )
        else:
            return bool(
                request.user.is_superuser or
                request.user.is_staff and request.method in permissions.SAFE_METHODS
            )


class IsAssociatedWithCustomerDiscount(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if hasattr(request.user, 'customer'):
            return bool(
                request.user.customer.customerdiscount_set.filter(pk=obj.pk).exists()
            )
        else:
            return bool(
                request.user.is_superuser or
                request.user.is_staff and request.method in permissions.SAFE_METHODS
            )
