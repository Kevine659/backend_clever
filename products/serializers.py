from rest_framework import serializers
from .models import Category, SubCategory, ProductRange, Product, ProductImage


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "image",
            "is_active",
            "created_at",
            "updated_at",
        ]


class SubCategorySerializer(serializers.ModelSerializer):

    category_name = serializers.CharField(
        source="category.name",
        read_only=True
    )

    class Meta:
        model = SubCategory
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "image",
            "category",
            "category_name",
            "is_active",
            "created_at",
            "updated_at",
        ]


class ProductRangeSerializer(serializers.ModelSerializer):

    products_count = serializers.IntegerField(
        source="products.count",
        read_only=True
    )

    class Meta:
        model = ProductRange

        fields = [
            "id",
            "name",
            "slug",
            "price",
            "description",
            "image",
            "is_active",
            "is_featured",
            "products_count",
            "created_at",
            "updated_at",
        ]


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage

        fields = [
            "id",
            "image",
            "alt_text",
            "is_primary",
            "created_at",
        ]


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.IntegerField(
        source="subcategory.category.id",
        read_only=True
    )

    category_name = serializers.CharField(
        source="subcategory.category.name",
        read_only=True
    )

    category_slug = serializers.CharField(
        source="subcategory.category.slug",
        read_only=True
    )
    subcategory_name = serializers.CharField(
        source="subcategory.name",
        read_only=True
    )

    subcategory_slug = serializers.CharField(
        source="subcategory.slug",
        read_only=True
    )

    product_range_name = serializers.CharField(
        source="product_range.name",
        read_only=True
    )

    product_range_slug = serializers.CharField(
        source="product_range.slug",
        read_only=True
    )

    product_range_image = serializers.ImageField(
        source="product_range.image",
        read_only=True
    )
    
    current_price = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        read_only=True
    )

    is_on_sale = serializers.BooleanField(
        read_only=True
    )

 

    images = ProductImageSerializer(
        many=True,
        read_only=True
    )

    class Meta:

        model = Product

        fields = [

            "id",
            "name",
            "slug",
            "reference",

            # catégorie
            "category",
            "category_name",
            "category_slug",

            # sous-catégorie
            "subcategory",
            "subcategory_name",
            "subcategory_slug",

            # gamme
            "product_range",
            "product_range_name",
            "product_range_slug",
            "product_range_image",

            # informations
            "description",
            "composition",
            "usage",
            "precautions",

            # prix
            "price",
            "promotional_price",
            "current_price",
            "is_on_sale",

            # stock
            "stock",

            # images
            "main_image",
            "images",

            # statut
            "is_active",
            "is_featured",

            "created_at",
            "updated_at",
        ]