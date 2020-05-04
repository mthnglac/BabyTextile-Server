from django.contrib import admin

from .models import Order, OrderShippingInformation, ProductPurchase


class ProductPurchaseInline(admin.TabularInline):
    model = ProductPurchase
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [ProductPurchaseInline]


admin.site.register(OrderShippingInformation)
