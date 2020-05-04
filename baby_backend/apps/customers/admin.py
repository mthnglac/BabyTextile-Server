from django.contrib import admin

from .models import (
    Customer,
    CustomerBillingAddress,
    CustomerDeliveryAddress,
    CustomerDiscount,
)


class CustomerDeliveryAddressInline(admin.TabularInline):
    model = CustomerDeliveryAddress
    extra = 1


class CustomerBillingAddressInline(admin.TabularInline):
    model = CustomerBillingAddress
    extra = 1


class CustomerDiscountInline(admin.TabularInline):
    model = CustomerDiscount
    extra = 1


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    inlines = [CustomerDeliveryAddressInline, CustomerBillingAddressInline, CustomerDiscountInline]


admin.site.register(CustomerDeliveryAddress)
admin.site.register(CustomerBillingAddress)
admin.site.register(CustomerDiscount)
