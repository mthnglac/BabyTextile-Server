from rest_framework import serializers

from .models import (
    Customer,
    CustomerBillingAddress,
    CustomerDeliveryAddress,
    CustomerDiscount,
)


class CustomerDiscountRootSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = CustomerDiscount
        fields = ['url', 'pk', 'customer', 'name', 'description', 'code', 'discount', 'is_active', 'valid_from',
                  'valid_until', 'num_uses', 'updated_at', 'created_at']


class CustomerDiscountSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = CustomerDiscount
        fields = ['url', 'pk', 'customer', 'name', 'description', 'code', 'discount', 'is_active', 'valid_from',
                  'valid_until', 'num_uses']


class CustomerDeliveryAddressRootSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = CustomerDeliveryAddress
        fields = ['url', 'pk', 'customer', 'title', 'is_active', 'address', 'zip_code', 'district', 'city',
                  'updated_at', 'created_at']


class CustomerDeliveryAddressSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = CustomerDeliveryAddress
        fields = ['url', 'pk', 'customer', 'title', 'is_active', 'address', 'zip_code', 'district', 'city']


class CustomerBillingAddressRootSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = CustomerBillingAddress
        fields = ['url', 'pk', 'customer', 'title', 'is_active', 'address', 'zip_code', 'district', 'city',
                  'billing_type', 'company_name', 'tax_number', 'tax_office', 'updated_at', 'created_at']


class CustomerBillingAddressSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = CustomerBillingAddress
        fields = ['url', 'pk', 'customer', 'title', 'is_active', 'address', 'zip_code', 'district', 'city',
                  'billing_type', 'company_name', 'tax_number', 'tax_office']


class CustomerRootSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Customer
        fields = ['url', 'pk', 'customer_id', 'user', 'tc_number', 'phone_number', 'customerdeliveryaddress_set',
                  'customerbillingaddress_set', 'customerdiscount_set', 'vendor', 'updated_at', 'created_at']
        extra_kwargs = {
            'customerdeliveryaddress_set': {'required': False},
            'customerbillingaddress_set': {'required': False},
            'customerdiscount_set': {'required': False}
        }


class CustomerVendorSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Customer
        fields = ['url', 'pk', 'user', 'tc_number', 'phone_number', 'customerdeliveryaddress_set',
                  'customerbillingaddress_set']
        extra_kwargs = {
            'customerdeliveryaddress_set': {'required': False},
            'customerbillingaddress_set': {'required': False},
        }


class CustomerSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Customer
        fields = ['url', 'pk', 'user', 'tc_number', 'phone_number', 'customerdeliveryaddress_set',
                  'customerbillingaddress_set']
        extra_kwargs = {
            'customerdeliveryaddress_set': {'required': False},
            'customerbillingaddress_set': {'required': False},
        }
