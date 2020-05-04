from django.contrib import admin
from .models import \
    Vendor, \
    VendorDeliveryAddress, \
    VendorBillingAddress, \
    VendorBankAccount, \
    VendorInstagram, \
    VendorBalance, \
    VendorDiscount, \
    VendorCustomer


class VendorDeliveryAddressInline(admin.TabularInline):
    model = VendorDeliveryAddress
    extra = 1


class VendorBillingAddressInline(admin.TabularInline):
    model = VendorBillingAddress
    extra = 1


class VendorBalanceInline(admin.TabularInline):
    model = VendorBalance
    extra = 1


class VendorInstagramInline(admin.TabularInline):
    model = VendorInstagram
    extra = 1


class VendorDiscountCodeInline(admin.TabularInline):
    model = VendorDiscount
    extra = 1


class VendorCustomerInline(admin.TabularInline):
    model = VendorCustomer
    extra = 1


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    inlines = [VendorDeliveryAddressInline, VendorBillingAddressInline, VendorDiscountCodeInline, VendorInstagramInline,
               VendorBalanceInline, VendorCustomerInline]


admin.site.register(VendorDeliveryAddress)
admin.site.register(VendorBillingAddress)
admin.site.register(VendorBankAccount)
admin.site.register(VendorBalance)
admin.site.register(VendorInstagram)
admin.site.register(VendorDiscount)
admin.site.register(VendorCustomer)
