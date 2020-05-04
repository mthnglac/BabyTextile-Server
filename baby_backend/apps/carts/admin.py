from django.contrib import admin
from .models import Cart, CartItem
# from ..orders.models import Order


# class OrderInline(admin.TabularInline):
#     model = Order
#     extra = 1


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]


admin.site.register(CartItem)
