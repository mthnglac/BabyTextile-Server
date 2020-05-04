from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ..accounts.permissions import IsStaffOrVendorReadOnly
from .models import (
    Product,
    ProductBrand,
    ProductCategory,
    ProductColor,
    ProductFile,
    ProductImage,
    ProductModel,
    ProductSize,
    ProductVAT,
)
from .serializers import (
    ProductBrandRootSerializer,
    ProductBrandSerializer,
    ProductCategoryRootSerializer,
    ProductCategorySerializer,
    ProductColorRootSerializer,
    ProductColorSerializer,
    ProductFileRootSerializer,
    ProductFileSerializer,
    ProductImageRootSerializer,
    ProductImageSerializer,
    ProductModelRootSerializer,
    ProductModelSerializer,
    ProductRootSerializer,
    ProductSerializer,
    ProductSizeRootSerializer,
    ProductSizeSerializer,
    ProductVATRootSerializer,
    ProductVATSerializer,
)


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated, IsStaffOrVendorReadOnly]

    def get_serializer_class(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return ProductRootSerializer
        return ProductSerializer


class ProductBrandViewSet(ModelViewSet):
    queryset = ProductBrand.objects.all()
    permission_classes = [IsAuthenticated, IsStaffOrVendorReadOnly]

    def get_serializer_class(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return ProductBrandRootSerializer
        return ProductBrandSerializer


class ProductModelViewSet(ModelViewSet):
    queryset = ProductModel.objects.all()
    permission_classes = [IsAuthenticated, IsStaffOrVendorReadOnly]

    def get_serializer_class(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return ProductModelRootSerializer
        return ProductModelSerializer


class ProductSizeViewSet(ModelViewSet):
    queryset = ProductSize.objects.all()
    permission_classes = [IsAuthenticated, IsStaffOrVendorReadOnly]

    def get_serializer_class(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return ProductSizeRootSerializer
        return ProductSizeSerializer


class ProductColorViewSet(ModelViewSet):
    queryset = ProductColor.objects.all()
    permission_classes = [IsAuthenticated, IsStaffOrVendorReadOnly]

    def get_serializer_class(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return ProductColorRootSerializer
        return ProductColorSerializer


class ProductCategoryViewSet(ModelViewSet):
    queryset = ProductCategory.objects.all()
    permission_classes = [IsAuthenticated, IsStaffOrVendorReadOnly]

    def get_serializer_class(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return ProductCategoryRootSerializer
        return ProductCategorySerializer


class ProductVATViewSet(ModelViewSet):
    queryset = ProductVAT.objects.all()
    permission_classes = [IsAuthenticated, IsStaffOrVendorReadOnly]

    def get_serializer_class(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return ProductVATRootSerializer
        return ProductVATSerializer


class ProductFileViewSet(ModelViewSet):
    queryset = ProductFile.objects.all()
    permission_classes = [IsAuthenticated, IsStaffOrVendorReadOnly]

    def get_serializer_class(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return ProductFileRootSerializer
        return ProductFileSerializer


class ProductImageViewSet(ModelViewSet):
    queryset = ProductImage.objects.all()
    permission_classes = [IsAuthenticated, IsStaffOrVendorReadOnly]

    def get_serializer_class(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return ProductImageRootSerializer
        return ProductImageSerializer
