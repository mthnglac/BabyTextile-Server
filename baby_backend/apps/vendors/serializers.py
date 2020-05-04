from rest_framework import serializers

from .models import (
    Vendor,
    VendorBalance,
    VendorBankAccount,
    VendorBillingAddress,
    VendorCustomer,
    VendorDeliveryAddress,
    VendorDiscount,
    VendorInstagram,
)


class VendorDeliveryAddressRootSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = VendorDeliveryAddress
        fields = ['url', 'pk', 'vendor', 'title', 'is_active', 'address', 'zip_code', 'district', 'city', 'updated_at',
                  'created_at']


class VendorDeliveryAddressSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = VendorDeliveryAddress
        fields = ['url', 'pk', 'vendor', 'title', 'is_active', 'address', 'zip_code', 'district', 'city']


class VendorBillingAddressRootSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = VendorBillingAddress
        fields = ['url', 'pk', 'vendor', 'title', 'is_active', 'address', 'zip_code', 'district', 'city',
                  'billing_type', 'company_name', 'tax_number', 'tax_office', 'updated_at', 'created_at']


class VendorBillingAddressSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = VendorBillingAddress
        fields = ['url', 'pk', 'vendor', 'title', 'is_active', 'address', 'zip_code', 'district', 'city',
                  'billing_type', 'company_name', 'tax_number', 'tax_office']


class VendorBankAccountRootSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = VendorBankAccount
        fields = ['url', 'pk', 'vendor', 'account_holder_first_name', 'account_holder_last_name', 'iban', 'updated_at',
                  'created_at']


class VendorBankAccountSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = VendorBankAccount
        fields = ['url', 'pk', 'vendor', 'account_holder_first_name', 'account_holder_last_name', 'iban']


class VendorInstagramRootSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = VendorInstagram
        fields = ['url', 'pk', 'vendor', 'username', 'old_username', 'followers_qty', 'old_followers_qty',
                  'follower_increase_rate', 'updated_at', 'created_at']


class VendorInstagramSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = VendorInstagram
        fields = ['url', 'pk', 'vendor', 'username', 'followers_qty']
        read_only_fields = ['followers_qty']


class VendorDiscountRootSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = VendorDiscount
        fields = ['url', 'pk', 'vendor', 'name', 'description', 'code', 'discount', 'is_active', 'valid_from',
                  'valid_until', 'num_uses', 'updated_at', 'created_at']


class VendorDiscountSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = VendorDiscount
        fields = ['url', 'pk', 'vendor', 'name', 'description', 'code', 'discount', 'valid_from', 'valid_until']
        read_only_fields = ['name', 'description', 'code', 'discount', 'valid_from', 'valid_until']


class VendorBalanceRootSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = VendorBalance
        fields = ['url', 'pk', 'vendor', 'subtotal_balance', 'withholding_tax_deduction', 'total_balance',
                  'paid_balance', 'money_demand', 'updated_at', 'created_at']


class VendorBalanceSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = VendorBalance
        fields = ['url', 'pk', 'vendor', 'subtotal_balance', 'withholding_tax_deduction', 'total_balance',
                  'paid_balance', 'money_demand']


class VendorRootSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Vendor
        fields = ['url', 'pk', 'vendor_id', 'user', 'tc_number', 'birth_date', 'birth_place', 'dealership_agreement',
                  'sms_request', 'email_request', 'commission_rate', 'total_sales_qty', 'total_sales_amount',
                  'sales_quota', 'vendorcustomer_set', 'vendordeliveryaddress_set', 'vendorbillingaddress_set',
                  'vendorbankaccount', 'vendorinstagram_set', 'vendordiscount_set', 'vendorbalance', 'updated_at',
                  'created_at']
        extra_kwargs = {
            'vendorcustomer_set': {'required': False},
            'vendordeliveryaddress_set': {"required": False},
            'vendorbillingaddress_set': {"required": False},
            'vendorbankaccount': {"required": False},
            'vendorinstagram_set': {"required": False},
            'vendordiscount_set': {"required": False},
            'vendorbalance': {"required": False},
        }


class VendorSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Vendor
        fields = ['url', 'pk', 'vendor_id', 'user', 'tc_number', 'birth_date', 'birth_place', 'dealership_agreement',
                  'sms_request', 'email_request', 'commission_rate', 'total_sales_qty', 'total_sales_amount',
                  'sales_quota', 'vendorcustomer_set', 'vendordeliveryaddress_set', 'vendorbillingaddress_set',
                  'vendorbankaccount', 'vendorinstagram_set', 'vendordiscount_set', 'vendorbalance']
        read_only_fields = ['vendor_id', 'commission_rate', 'total_sales_qty', 'total_sales_amount', 'sales_quota']


class VendorCustomerRootSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = VendorCustomer
        fields = ['url', 'pk', 'vendor', 'first_name', 'last_name', 'phone_number', 'zip_code', 'district', 'city',
                  'address', 'updated_at', 'created_at']


class VendorCustomerSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = VendorCustomer
        fields = ['url', 'pk', 'vendor', 'first_name', 'last_name', 'phone_number', 'zip_code', 'district', 'city',
                  'address']
