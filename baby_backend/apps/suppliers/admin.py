from django.contrib import admin

from .models import Supplier, SupplierDeliveryAddress

admin.site.register(Supplier)
admin.site.register(SupplierDeliveryAddress)
