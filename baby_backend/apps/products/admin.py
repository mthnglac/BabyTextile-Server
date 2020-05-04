from django.contrib import admin

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


class ProductFileInline(admin.TabularInline):
    model = ProductFile
    extra = 1


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductModelInline(admin.TabularInline):
    model = ProductModel
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]


@admin.register(ProductBrand)
class ProductBrandAdmin(admin.ModelAdmin):
    inlines = [ProductModelInline]


admin.site.register(ProductModel)
admin.site.register(ProductCategory)
admin.site.register(ProductFile)
admin.site.register(ProductImage)
admin.site.register(ProductSize)
admin.site.register(ProductColor)
admin.site.register(ProductVAT)
