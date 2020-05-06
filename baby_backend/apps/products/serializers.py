from rest_framework import serializers
from taggit_serializer.serializers import TaggitSerializer, TagListSerializerField

from ..products.models import (
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


class ProductFileRootSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ProductFile
        fields = ['url', 'pk', 'product', 'name', 'file', 'updated_at', 'created_at']


class ProductFileSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ProductFile
        fields = ['url', 'pk', 'product', 'name', 'file']


class ProductImageRootSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ProductImage
        fields = ['url', 'pk', 'product', 'name', 'image', 'updated_at', 'created_at']


class ProductImageSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ProductImage
        fields = ['url', 'pk', 'product', 'name', 'image']


class ProductSizeRootSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ProductSize
        fields = ['url', 'pk', 'start_month', 'end_month', 'age', 'size', 'updated_at', 'created_at']


class ProductSizeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ProductSize
        fields = ['url', 'pk', 'start_month', 'end_month', 'age', 'size']


class ProductColorRootSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ProductColor
        fields = ['url', 'pk', 'name', 'updated_at', 'created_at']


class ProductColorSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ProductColor
        fields = ['url', 'pk', 'name']


class ProductVATRootSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ProductVAT
        fields = ['url', 'pk', 'vat_rate', 'updated_at', 'created_at']


class ProductVATSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ProductVAT
        fields = ['url', 'pk', 'vat_rate']


class ProductCategoryRootSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ProductCategory
        fields = ['url', 'pk', 'name', 'description', 'active', 'meta_keywords', 'meta_description', 'updated_at',
                  'created_at']


class ProductCategorySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ProductCategory
        fields = ['url', 'pk', 'name', 'description', 'active', 'meta_keywords', 'meta_description']


class ProductModelRootSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ProductModel
        fields = ['url', 'pk', 'name', 'updated_at', 'created_at']


class ProductModelSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ProductModel
        fields = ['url', 'pk', 'brand', 'name']


class ProductBrandRootSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ProductBrand
        fields = ['url', 'pk', 'name', 'updated_at', 'created_at']


class ProductBrandSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ProductBrand
        fields = ['url', 'pk', 'name']


class ProductRootSerializer(TaggitSerializer, serializers.HyperlinkedModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        model = Product
        fields = ['url', 'pk', 'product_unique_id', 'name', 'active', 'featured', 'best_seller', 'tags',
                  'brand_information', 'model_information', 'sku', 'description', 'size', 'color', 'purchase_price',
                  'old_purchase_price', 'sale_price', 'old_sale_price', 'vat', 'category', 'supplier', 'sold_qty',
                  'purchased_stock', 'available_stock', 'meta_keywords', 'meta_description', 'productimage_set',
                  'productfile_set', 'updated_at', 'created_at']
        extra_kwargs = {
            'productimage_set': {'required': False},
            'productfile_set': {'required': False},
            'supplier': {'required': False}
        }


class ProductSerializer(TaggitSerializer, serializers.HyperlinkedModelSerializer):
    tags = TagListSerializerField(read_only=True)

    class Meta:
        model = Product
        fields = ['url', 'pk', 'product_unique_id', 'name', 'active', 'featured', 'best_seller', 'tags',
                  'brand_information', 'model_information', 'sku', 'description', 'size', 'color', 'purchase_price',
                  'old_purchase_price', 'sale_price', 'old_sale_price', 'vat', 'category', 'supplier', 'sold_qty',
                  'purchased_stock', 'available_stock', 'meta_keywords', 'meta_description', 'productimage_set',
                  'productfile_set']
        extra_kwargs = {
            'productimage_set': {'required': False},
            'productfile_set': {'required': False},
            'supplier': {'required': False}
        }
