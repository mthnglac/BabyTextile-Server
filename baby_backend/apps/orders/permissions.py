from rest_framework import permissions


class IsVendorAssociatedWithOrder(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if hasattr(request.user, 'vendor'):
            return bool(
                obj.billing_profile == request.user.billing_profile
            )
        else:
            return bool(
                request.user.is_superuser or
                request.user.is_staff and request.method in permissions.SAFE_METHODS
            )


class IsVendorAssociatedWithOrderShipping(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if hasattr(request.user, 'vendor'):
            return bool(
                request.user.billing_profile.order_set.filter(shipping_information=obj).exists()
            )
        else:
            return bool(
                request.user.is_superuser or
                request.user.is_staff and request.method in permissions.SAFE_METHODS
            )


class IsVendorAssociatedWithOrderShippingMovement(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if hasattr(request.user, 'vendor'):
            return bool(
                request.user.billing_profile.order_set.filter(shipping_information__ordershippingmovement=obj).exists()
            )
        else:
            return bool(
                request.user.is_superuser or
                request.user.is_staff and request.method in permissions.SAFE_METHODS
            )


class IsVendorAssociatedWithProductPurchase(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if hasattr(request.user, 'vendor'):
            return bool(
                request.user.billing_profile.order_set.filter(productpurchase=obj).exists()
            )
        else:
            return bool(
                request.user.is_superuser or
                request.user.is_staff and request.method in permissions.SAFE_METHODS
            )
