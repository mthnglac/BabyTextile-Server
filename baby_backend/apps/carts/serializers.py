from rest_framework import serializers

from .models import Cart, CartItem


class CartRootSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Cart
        fields = ['url', 'pk', 'cart_id', 'user', 'qty', 'subtotal', 'total',
                  'cartitem_set', 'updated_at', 'created_at']
        extra_kwargs = {
            'cartitem_set': {'required': False}
        }


class CartSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Cart
        fields = ['url', 'pk', 'cart_id', 'user', 'qty', 'subtotal', 'total', 'cartitem_set']
        read_only_fields = ['url', 'pk', 'cart_id', 'user', 'qty', 'subtotal', 'total', 'cartitem_set']
        extra_kwargs = {
            'cartitem_set': {'required': False}
        }


class CartItemRootSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = CartItem
        fields = ['url', 'pk', 'item_id', 'cart', 'product', 'qty', 'line_total', 'updated_at', 'created_at']


class CartItemSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = CartItem
        fields = ['url', 'pk', 'item_id', 'cart', 'product', 'qty', 'line_total']
        read_only_fields = ['url', 'pk', 'item_id', 'line_total']
