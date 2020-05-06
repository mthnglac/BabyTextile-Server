from django.contrib import admin

from .models import Supplier, SupplierBillingAddress, SupplierDeliveryAddress

admin.site.register(Supplier)
admin.site.register(SupplierDeliveryAddress)
admin.site.register(SupplierBillingAddress)
