from rest_framework import serializers

from .models import Supplier, SupplierDeliveryAddress, SupplierBillingAddress


class SupplierRootSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Supplier
        fields = ['url', 'pk', 'company_name', 'tax_number', 'phone_number', 'total_purchase_amount', 'paid_amount',
                  'unpaid_amount', 'supplierdeliveryaddress_set', 'supplierdeliveryaddress_set', 'updated_at',
                  'created_at']
        extra_kwargs = {
            'supplierdeliveryaddress_set': {'required': False},
            'supplierbillingaddress_set': {'required': False}
        }


class SupplierSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Supplier
        fields = ['url', 'pk', 'company_name', 'tax_number', 'phone_number', 'total_purchase_amount', 'paid_amount',
                  'unpaid_amount', 'supplierdeliveryaddress_set', 'supplierbillingaddress_set']
        extra_kwargs = {
            'supplierdeliveryaddress_set': {'required': False},
            'supplierbillingaddress_set': {'required': False}
        }


class SupplierDeliveryAddressRootSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = SupplierDeliveryAddress
        fields = ['url', 'pk', 'supplier', 'is_active', 'title', 'address', 'zip_code', 'district', 'city', 'country',
                  'updated_at', 'created_at']


class SupplierDeliveryAddressSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = SupplierDeliveryAddress
        fields = ['url', 'pk', 'supplier', 'is_active', 'title', 'address', 'zip_code', 'district', 'city', 'country']


class SupplierBillingAddressRootSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = SupplierBillingAddress
        fields = ['url', 'pk', 'supplier', 'is_active', 'title', 'address', 'zip_code', 'district', 'city',
                  'billing_type', 'company_name', 'tax_number', 'tax_office', 'updated_at', 'created_at']


class SupplierBillingAddressSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = SupplierBillingAddress
        fields = ['url', 'pk', 'supplier', 'is_active', 'title', 'address', 'zip_code', 'district', 'city',
                  'country', 'company_name', 'tax_number', 'tax_office']
