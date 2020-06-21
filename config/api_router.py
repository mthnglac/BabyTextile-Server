from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from baby_backend.apps.accounts.views import UserViewSet
from baby_backend.apps.billing.views import BillingProfileViewSet  # and ChargeViewSet
from baby_backend.apps.carts.views import CartItemViewSet, CartViewSet
from baby_backend.apps.customers.views import (
    CustomerBillingAddressViewSet,
    CustomerDeliveryAddressViewSet,
    CustomerDiscountViewSet,
    CustomerViewSet,
)
from baby_backend.apps.guests.views import GuestVendorViewSet
from baby_backend.apps.orders.views import (
    OrderShippingInformationViewSet,
    OrderShippingMovementViewSet,
    OrderViewSet,
    ProductPurchaseViewSet,
)
from baby_backend.apps.products.views import (
    ProductBrandViewSet,
    ProductCategoryViewSet,
    ProductColorViewSet,
    ProductFileViewSet,
    ProductImageViewSet,
    ProductModelViewSet,
    ProductSizeViewSet,
    ProductVATViewSet,
    ProductViewSet,
    ProductVariantViewSet,
)
from baby_backend.apps.suppliers.views import (
    SupplierBillingAddressViewSet,
    SupplierDeliveryAddressViewSet,
    SupplierViewSet,
)
from baby_backend.apps.vendors.views import (
    VendorBalanceViewSet,
    VendorBankAccountViewSet,
    VendorBillingAddressViewSet,
    VendorCustomerViewSet,
    VendorDeliveryAddressViewSet,
    VendorDiscountViewSet,
    VendorInstagramViewSet,
    VendorViewSet,
)

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()


router.register(r'users', UserViewSet)
router.register(r'billing', BillingProfileViewSet)
# router.register(r'charge', ChargeViewSet)
router.register(r'carts', CartViewSet)
router.register(r'cart-items', CartItemViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'customer-delivery-addresses', CustomerDeliveryAddressViewSet)
router.register(r'customer-billing-addresses', CustomerBillingAddressViewSet)
router.register(r'customer-discounts', CustomerDiscountViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'order-shipping-address-information', OrderShippingInformationViewSet)
router.register(r'order-shipping-movement', OrderShippingMovementViewSet)
router.register(r'order-product-purchases', ProductPurchaseViewSet)
router.register(r'products', ProductViewSet)
router.register(r'product-brands', ProductBrandViewSet)
router.register(r'product-models', ProductModelViewSet)
router.register(r'product-sizes', ProductSizeViewSet)
router.register(r'product-colors', ProductColorViewSet)
router.register(r'product-categories', ProductCategoryViewSet)
router.register(r'product-vats', ProductVATViewSet)
router.register(r'product-files', ProductFileViewSet)
router.register(r'product-images', ProductImageViewSet)
router.register(r'product-variants', ProductVariantViewSet)
router.register(r'suppliers', SupplierViewSet)
router.register(r'supplier-delivery-addresses', SupplierDeliveryAddressViewSet)
router.register(r'supplier-billing-addresses', SupplierBillingAddressViewSet)
router.register(r'vendors', VendorViewSet)
router.register(r'vendor-bank-accounts', VendorBankAccountViewSet)
router.register(r'vendor-delivery-addresses', VendorDeliveryAddressViewSet)
router.register(r'vendor-billing-addresses', VendorBillingAddressViewSet)
router.register(r'vendor-instagrams', VendorInstagramViewSet)
router.register(r'vendor-discounts', VendorDiscountViewSet)
router.register(r'vendor-balance', VendorBalanceViewSet)
router.register(r'vendor-customer', VendorCustomerViewSet)
router.register(r'guests', GuestVendorViewSet)


# app_name = "api"
urlpatterns = router.urls
