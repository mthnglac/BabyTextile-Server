from django.utils.translation import ugettext_lazy as _
from rest_framework.throttling import UserRateThrottle
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from ..accounts.permissions import IsStaffReadOnlyOrVendorRestricted, \
    IsStaffOrVendor, IsStaffOrVendorReadOnly, IsStaffReadOnlyOrVendorPostOnly, IsStaffReadOnlyOrCustomer, \
    IsStaffReadOnlyOrVendor, IsStaffReadOnlyOrVendorReadOnly
from .permissions import \
    IsAssociatedWithVendor, \
    IsAssociatedWithBankAccount, \
    IsAssociatedWithVendorDeliveryAddress, \
    IsAssociatedWithVendorBillingAddress, \
    IsAssociatedWithInstagram, \
    IsAssociatedWithDiscount, \
    IsAssociatedWithBalance, \
    IsAssociatedWithVendorCustomer
from .serializers import \
    VendorSerializer, \
    VendorRootSerializer, \
    VendorBankAccountSerializer, \
    VendorBankAccountRootSerializer, \
    VendorDeliveryAddressSerializer, \
    VendorDeliveryAddressRootSerializer, \
    VendorBillingAddressSerializer, \
    VendorBillingAddressRootSerializer, \
    VendorInstagramSerializer, \
    VendorInstagramRootSerializer, \
    VendorDiscountRootSerializer, \
    VendorDiscountSerializer, \
    VendorBalanceSerializer, \
    VendorBalanceRootSerializer, \
    VendorCustomerSerializer, \
    VendorCustomerRootSerializer
from .models import \
    Vendor, \
    VendorBankAccount, \
    VendorDeliveryAddress, \
    VendorBillingAddress, \
    VendorInstagram, \
    VendorDiscount, \
    VendorBalance, \
    VendorCustomer


class VendorViewSet(ModelViewSet):
    queryset = Vendor.objects.all()
    permission_classes = [IsAuthenticated, IsStaffReadOnlyOrVendorRestricted, IsAssociatedWithVendor]

    def get_serializer_class(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return VendorRootSerializer
        return VendorSerializer

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            qs = Vendor.objects.all()
        else:
            qs = Vendor.objects.filter(pk=self.request.user.vendor.pk)
        return qs


class VendorBankAccountViewSet(ModelViewSet):
    queryset = VendorBankAccount.objects.all()
    permission_classes = [IsAuthenticated, IsStaffReadOnlyOrVendorRestricted, IsAssociatedWithBankAccount]

    def get_serializer_class(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return VendorBankAccountRootSerializer
        return VendorBankAccountSerializer

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            qs = VendorBankAccount.objects.all()
        else:
            qs = VendorBankAccount.objects.filter(vendor=self.request.user.vendor)
        return qs


class VendorDeliveryAddressViewSet(ModelViewSet):
    queryset = VendorDeliveryAddress.objects.all()
    permission_classes = [IsAuthenticated, IsStaffReadOnlyOrVendor, IsAssociatedWithVendorDeliveryAddress]

    def perform_create(self, serializer):
        if hasattr(self.request.user, 'vendor') and self.request.user.vendor.vendordeliveryaddress_set.count() > 3:
            raise PermissionDenied({'message': _('You can add up to three addresses.')})
        else:
            serializer.save()

    def get_serializer_class(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return VendorDeliveryAddressRootSerializer
        return VendorDeliveryAddressSerializer

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            qs = VendorDeliveryAddress.objects.all()
        else:
            qs = VendorDeliveryAddress.objects.filter(vendor=self.request.user.vendor)
        return qs


class VendorBillingAddressViewSet(ModelViewSet):
    queryset = VendorBillingAddress.objects.all()
    permission_classes = [IsAuthenticated, IsStaffReadOnlyOrVendor, IsAssociatedWithVendorBillingAddress]

    def perform_create(self, serializer):
        if hasattr(self.request.user, 'vendor') \
                and self.request.user.vendor.vendorbillingaddress_set.count() > 3:
            raise PermissionDenied({'message': _('You can add up to three billing addresses.')})
        else:
            serializer.save()

    def get_serializer_class(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return VendorBillingAddressRootSerializer
        else:
            return VendorBillingAddressSerializer

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            qs = VendorBillingAddress.objects.all()
        else:
            qs = VendorBillingAddress.objects.filter(vendor=self.request.user.vendor)
        return qs


class VendorInstagramViewSet(ModelViewSet):
    queryset = VendorInstagram.objects.all()
    permission_classes = [IsAuthenticated, IsStaffReadOnlyOrVendor, IsAssociatedWithInstagram]

    def perform_create(self, serializer):
        if hasattr(self.request.user, 'vendor') and self.request.user.vendor.vendorinstagram_set.count() > 3:
            raise PermissionDenied({'message': _('You can add up to three instagram addresses.')})
        else:
            serializer.save()

    def get_serializer_class(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return VendorInstagramRootSerializer
        return VendorInstagramSerializer

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            qs = VendorInstagram.objects.all()
        else:
            qs = VendorInstagram.objects.filter(vendor=self.request.user.vendor)
        return qs


class VendorDiscountViewSet(ModelViewSet):
    queryset = VendorDiscount.objects.all()
    permission_classes = [IsAuthenticated, IsStaffReadOnlyOrVendorReadOnly, IsAssociatedWithDiscount]

    def get_serializer_class(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return VendorDiscountRootSerializer
        return VendorDiscountSerializer

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            qs = VendorDiscount.objects.all()
        else:
            qs = VendorDiscount.objects.filter(vendor=self.request.user.vendor)
        return qs


class VendorBalanceViewSet(ModelViewSet):
    queryset = VendorBalance.objects.all()
    permission_classes = [IsAuthenticated, IsStaffReadOnlyOrVendorReadOnly, IsAssociatedWithBalance]

    def get_serializer_class(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return VendorBalanceRootSerializer
        return VendorBalanceSerializer

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            qs = VendorBalance.objects.all()
        else:
            qs = VendorBalance.objects.filter(vendor=self.request.user.vendor)
        return qs


class VendorCustomerViewSet(ModelViewSet):
    queryset = VendorCustomer.objects.all()
    permission_classes = [IsAuthenticated, IsStaffReadOnlyOrVendorPostOnly, IsAssociatedWithVendorCustomer]

    def get_throttles(self):
        if hasattr(self.request.user, 'vendor') and self.request.method == 'POST':
            return [throttle() for throttle in [UserRateThrottle]]
        else:
            return super(VendorCustomerViewSet, self).get_throttles()

    def get_serializer_class(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return VendorCustomerRootSerializer
        return VendorCustomerSerializer

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            qs = VendorCustomer.objects.all()
        else:
            qs = VendorCustomer.objects.filter(vendor=self.request.user.vendor)
        return qs
