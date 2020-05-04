from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import NotFound

from .models import (
    Order,
    OrderShippingInformation,
    OrderShippingMovement,
    ProductPurchase,
)


class OrderShippingInformationRootSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = OrderShippingInformation
        fields = ['url', 'pk', 'customer', 'description', 'payment_method', 'shipping_company', 'shipping_total',
                  'tracking_number', 'updated_at', 'created_at']


class OrderShippingInformationVendorSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = OrderShippingInformation
        fields = ['url', 'vendor_customer', 'description', 'payment_method', 'shipping_company', 'shipping_total',
                  'tracking_number']


class OrderShippingInformationSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = OrderShippingInformation
        fields = ['url', 'customer', 'description', 'payment_method', 'shipping_company', 'shipping_total',
                  'tracking_number']


class OrderShippingMovementRootSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = OrderShippingMovement
        fields = ['url', 'pk', 'shipping_information', 'title', 'subtitle', 'updated_at', 'created_at']


class OrderShippingMovementSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = OrderShippingMovement
        fields = ['url', 'pk', 'shipping_information', 'title', 'subtitle']


class ProductPurchaseRootSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ProductPurchase
        fields = ['url', 'pk', 'product', 'product_price', 'qty', 'line_total', 'order', 'refunded', 'updated_at',
                  'created_at']


class ProductPurchaseSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ProductPurchase
        fields = ['url', 'product', 'product_price', 'qty', 'line_total', 'order', 'refunded']


class OrderRootSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Order
        fields = ['url', 'pk', 'order_id', 'billing_profile', 'shipping_information', 'total_amount', 'cart', 'status',
                  'active', 'discount_code', 'commission_amount', 'ip_address', 'productpurchase_set', 'updated_at',
                  'created_at']
        extra_kwargs = {
           'productpurchase_set': {'required': False}
        }

    def validate(self, attrs):
        cart_items_qs = attrs.get('cart').cartitem_set
        if not cart_items_qs.exists():
            raise NotFound(
                detail={
                    'message': _('You must have items in your cart to complete your shopping.')
                }
            )
        return attrs


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    ip_address = serializers.IPAddressField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Order
        fields = ['url', 'pk', 'order_id', 'billing_profile', 'shipping_information', 'total_amount', 'cart', 'status',
                  'active', 'discount_code', 'commission_amount', 'ip_address', 'productpurchase_set']
        extra_kwargs = {
           'productpurchase_set': {'required': False}
        }

    def validate(self, attrs):
        cart_items_qs = attrs.get('cart').cartitem_set
        if not cart_items_qs.exists():
            raise NotFound(
                detail={
                    'message': _('You must have items in your cart to complete your shopping.')
                }
            )
        return attrs
