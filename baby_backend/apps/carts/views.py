from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ..accounts.permissions import IsReadOnly, IsStaffReadOnlyOrVendor
from .models import Cart, CartItem
from .serializers import (
    CartItemRootSerializer,
    CartItemSerializer,
    CartRootSerializer,
    CartSerializer,
)


class CartViewSet(ModelViewSet):
    queryset = Cart.objects.all()
    permission_classes = [IsAuthenticated, IsReadOnly]

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            qs = Cart.objects.all()
        else:
            qs = Cart.objects.filter(user=self.request.user)
        return qs

    def get_serializer_class(self):
        if self.request.user.is_superuser:
            return CartRootSerializer
        return CartSerializer


class CartItemViewSet(ModelViewSet):
    queryset = CartItem.objects.all()
    permission_classes = [IsAuthenticated, IsStaffReadOnlyOrVendor]

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            qs = CartItem.objects.all()
        else:
            qs = CartItem.objects.filter(cart=self.request.user.cart)
        return qs

    def get_serializer_class(self):
        if self.request.user.is_superuser:
            return CartItemRootSerializer
        return CartItemSerializer
