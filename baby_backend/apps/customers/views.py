from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ..accounts.permissions import (
    IsStaffReadOnlyOrCustomer,
    IsStaffReadOnlyOrCustomerReadOnly,
    IsStaffReadOnlyOrCustomerRestricted,
)
from .models import (
    Customer,
    CustomerBillingAddress,
    CustomerDeliveryAddress,
    CustomerDiscount,
)
from .permissions import (
    IsAssociatedWithCustomer,
    IsAssociatedWithCustomerBillingAddress,
    IsAssociatedWithCustomerDeliveryAddress,
    IsAssociatedWithCustomerDiscount,
)
from .serializers import (
    CustomerBillingAddressRootSerializer,
    CustomerBillingAddressSerializer,
    CustomerDeliveryAddressRootSerializer,
    CustomerDeliveryAddressSerializer,
    CustomerDiscountRootSerializer,
    CustomerDiscountSerializer,
    CustomerRootSerializer,
    CustomerSerializer,
)


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    permission_classes = [IsAuthenticated, IsStaffReadOnlyOrCustomerRestricted, IsAssociatedWithCustomer]

    def get_serializer_class(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return CustomerRootSerializer
        else:
            return CustomerSerializer

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            qs = Customer.objects.all()
        else:
            # istek attiginda butun customer'lari gormesin diye. sadece kendini gorsun.
            qs = Customer.objects.filter(user=self.request.user)
        return qs


class CustomerDeliveryAddressViewSet(ModelViewSet):
    queryset = CustomerDeliveryAddress.objects.all()
    permission_classes = [IsAuthenticated, IsStaffReadOnlyOrCustomer, IsAssociatedWithCustomerDeliveryAddress]

    def perform_create(self, serializer):
        if hasattr(self.request.user, 'customer') \
                and self.request.user.customer.customerdeliveryaddress_set.count() > 3:
            raise PermissionDenied({'message': _('You can add up to three addresses.')})
        else:
            serializer.save()

    def get_serializer_class(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return CustomerDeliveryAddressRootSerializer
        return CustomerDeliveryAddressSerializer

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            qs = CustomerDeliveryAddress.objects.all()
        else:
            qs = CustomerDeliveryAddress.objects.filter(customer__user=self.request.user)
        return qs


class CustomerBillingAddressViewSet(ModelViewSet):
    queryset = CustomerBillingAddress.objects.all()
    permission_classes = [IsAuthenticated, IsStaffReadOnlyOrCustomer, IsAssociatedWithCustomerBillingAddress]

    def perform_create(self, serializer):
        if hasattr(self.request.user, 'customer') \
                and self.request.user.customer.customerbillingaddress_set.count() > 3:
            raise PermissionDenied({'message': _('You can add up to three billing addresses.')})
        else:
            serializer.save()

    def get_serializer_class(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return CustomerBillingAddressRootSerializer
        else:
            return CustomerBillingAddressSerializer

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            qs = CustomerBillingAddress.objects.all()
        else:
            qs = CustomerBillingAddress.objects.filter(customer__user=self.request.user)
        return qs


class CustomerDiscountViewSet(ModelViewSet):
    queryset = CustomerDiscount.objects.all()
    permission_classes = [IsAuthenticated, IsStaffReadOnlyOrCustomerReadOnly, IsAssociatedWithCustomerDiscount]

    def get_serializer_class(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return CustomerDiscountRootSerializer
        return CustomerDiscountSerializer

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            qs = CustomerDiscount.objects.all()
        else:
            qs = CustomerDiscount.objects.filter(customer__user=self.request.user)
        return qs
