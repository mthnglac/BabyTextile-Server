from django.contrib import admin

from ..orders.models import Order
from .models import BillingProfile, Charge


class OrderInline(admin.TabularInline):
    model = Order
    extra = 1


class ChargeInline(admin.TabularInline):
    model = Charge
    extra = 1


@admin.register(BillingProfile)
class BillingProfileAdmin(admin.ModelAdmin):
    inlines = [ChargeInline, OrderInline]


admin.site.register(Charge)
