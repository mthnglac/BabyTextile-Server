from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from ..accounts.permissions import IsStaffUser

from .models import Supplier, SupplierDeliveryAddress, SupplierBillingAddress
from .serializers import \
    SupplierSerializer, \
    SupplierRootSerializer, \
    SupplierDeliveryAddressSerializer, \
    SupplierDeliveryAddressRootSerializer, \
    SupplierBillingAddressSerializer, \
    SupplierBillingAddressRootSerializer


class SupplierViewSet(ModelViewSet):
    queryset = Supplier.objects.all()
    permission_classes = [IsAuthenticated, IsStaffUser]

    def get_serializer_class(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return SupplierRootSerializer
        return SupplierSerializer


class SupplierDeliveryAddressViewSet(ModelViewSet):
    queryset = SupplierDeliveryAddress.objects.all()
    permission_classes = [IsAuthenticated, IsStaffUser]

    def get_serializer_class(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return SupplierDeliveryAddressRootSerializer
        return SupplierDeliveryAddressSerializer


class SupplierBillingAddressViewSet(ModelViewSet):
    queryset = SupplierBillingAddress.objects.all()
    permission_classes = [IsAuthenticated, IsStaffUser]

    def get_serializer_class(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return SupplierBillingAddressRootSerializer
        else:
            return SupplierBillingAddressSerializer
