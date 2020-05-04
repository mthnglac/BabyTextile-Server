from ..apps.products.models import (
    Product,
    ProductBrand,
    ProductCategory,
    ProductColor,
    ProductModel,
    ProductSize,
    ProductVAT,
)


def deletion():
    Product.objects.all().delete()
    ProductVAT.objects.all().delete()
    ProductBrand.objects.all().delete()
    ProductModel.objects.all().delete()
    ProductSize.objects.all().delete()
    ProductColor.objects.all().delete()
    ProductCategory.objects.all().delete()
