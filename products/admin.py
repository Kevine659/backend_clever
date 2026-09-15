from django.contrib import admin
from .models import (Category,SubCategory,Product, ProductImage,ProductRange)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ( "name", "is_active", "created_at",)
    list_filter = ("is_active","created_at",)
    search_fields = ("name", )

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ( "name", "category", "is_active",  "created_at", )
    list_filter = ("category","is_active",)
    search_fields = ("name","category__name",)

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(ProductRange)
class ProductRangeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "price",
        "is_active",
        "is_featured",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "is_active",
        "is_featured",
    )

    search_fields = (
        "name",
        "slug",
        "description",
    )

    list_editable = (
        "price",
        "is_active",
        "is_featured",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Informations générales",
            {
                "fields": (
                    "name",
                    "slug",
                    "description",
                    "price",
                )
            },
        ),
        (
            "Image",
            {
                "fields": (
                    "image",
                )
            },
        ),
        (
            "Visibilité",
            {
                "fields": (
                    "is_active",
                    "is_featured",
                )
            },
        ),
        (
            "Dates",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "reference",
        "subcategory",
        "product_range",
        "price",
        "promotional_price",
        "stock",
        "is_active",
        "is_featured",
        "created_at",
    )

    list_filter = (
        "is_active",
        "is_featured",
        "subcategory",
        "subcategory__category",
        "product_range",
    )

    search_fields = (
        "name",
        "slug",
        "reference",
        "description",
    )

    list_editable = (
        "price",
        "promotional_price",
        "stock",
        "is_active",
        "is_featured",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    inlines = [
        ProductImageInline,
    ]

    fieldsets = (
        (
            "Informations générales",
            {
                "fields": (
                    "name",
                    "slug",
                    "reference",
                    "subcategory",
                    "product_range",
                    "description",
                )
            },
        ),
        (
            "Informations complémentaires",
            {
                "fields": (
                    "composition",
                    "usage",
                    "precautions",
                )
            },
        ),
        (
            "Prix et stock",
            {
                "fields": (
                    "price",
                    "promotional_price",
                    "stock",
                )
            },
        ),
        (
            "Image",
            {
                "fields": (
                    "main_image",
                )
            },
        ),
        (
            "Visibilité",
            {
                "fields": (
                    "is_active",
                    "is_featured",
                )
            },
        ),
        (
            "Dates",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "is_primary",
        "created_at",
    )

    list_filter = (
        "is_primary",
    )

    search_fields = (
        "product__name",
    )