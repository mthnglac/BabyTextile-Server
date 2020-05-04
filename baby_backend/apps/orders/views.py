from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ..accounts.permissions import (
    IsHaveBillingProfile,
    IsStaffReadOnlyOrVendorPostOnly,
    IsStaffReadOnlyOrVendorReadOnly,
)
from .models import (
    Order,
    OrderShippingInformation,
    OrderShippingMovement,
    ProductPurchase,
)
from .permissions import (
    IsVendorAssociatedWithOrder,
    IsVendorAssociatedWithOrderShipping,
    IsVendorAssociatedWithOrderShippingMovement,
    IsVendorAssociatedWithProductPurchase,
)
from .serializers import (
    OrderRootSerializer,
    OrderSerializer,
    OrderShippingInformationRootSerializer,
    OrderShippingInformationSerializer,
    OrderShippingInformationVendorSerializer,
    OrderShippingMovementRootSerializer,
    OrderShippingMovementSerializer,
    ProductPurchaseRootSerializer,
    ProductPurchaseSerializer,
)


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated, IsStaffReadOnlyOrVendorPostOnly, IsHaveBillingProfile,
                          IsVendorAssociatedWithOrder]

    def perform_create(self, serializer):
        client_ip_data = self.get_client_ip()
        serializer.save(ip_address=client_ip_data)

    def get_serializer_class(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return OrderRootSerializer
        return OrderSerializer

    def get_queryset(self):
        if hasattr(self.request.user, 'vendor'):
            # by_request --> filtering based on request.user.billing_profile.
            # If not exists, create one.
            qs = Order.objects.by_request(self.request)
        else:
            qs = Order.objects.all()  # for superuser and staff users
        return qs

    def get_client_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR', None)
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip


class OrderShippingInformationViewSet(ModelViewSet):
    queryset = OrderShippingInformation.objects.all()
    permission_classes = [IsAuthenticated, IsStaffReadOnlyOrVendorPostOnly, IsHaveBillingProfile,
                          IsVendorAssociatedWithOrderShipping]

    def get_serializer_class(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return OrderShippingInformationRootSerializer
        elif hasattr(self.request.user, 'vendor'):
            return OrderShippingInformationVendorSerializer
        else:
            return OrderShippingInformationSerializer

    def get_queryset(self):
        if hasattr(self.request.user, 'vendor'):
            qs = OrderShippingInformation.objects.filter(
                order__in=self.request.user.billing_profile.order_set.all()
            )
        else:
            qs = OrderShippingInformation.objects.all()  # for superuser and staff users
        return qs


class OrderShippingMovementViewSet(ModelViewSet):
    queryset = OrderShippingMovement.objects.all()
    permission_classes = [IsAuthenticated, IsStaffReadOnlyOrVendorReadOnly, IsHaveBillingProfile,
                          IsVendorAssociatedWithOrderShippingMovement]

    def get_serializer_class(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return OrderShippingMovementRootSerializer
        return OrderShippingMovementSerializer

    def get_queryset(self):
        if hasattr(self.request.user, 'vendor'):
            qs = OrderShippingMovement.objects.filter(
                shipping_information__in=self.request.user.billing_profile.order_set.all()
            )
        else:
            qs = OrderShippingMovement.objects.all()  # for superuser and staff users
        return qs


class ProductPurchaseViewSet(ModelViewSet):
    queryset = ProductPurchase.objects.all()
    permission_classes = [IsAuthenticated, IsStaffReadOnlyOrVendorReadOnly, IsHaveBillingProfile,
                          IsVendorAssociatedWithProductPurchase]

    def get_serializer_class(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return ProductPurchaseRootSerializer
        return ProductPurchaseSerializer

    def get_queryset(self):
        if hasattr(self.request.user, 'vendor'):
            qs = ProductPurchase.objects.filter(order__in=self.request.user.billing_profile.order_set.all())
        else:
            qs = ProductPurchase.objects.all()  # for superuser and staff users
        return qs
