import django_filters
from django.db import models
from .models import Product

class ProductFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(
        method="filter_search"
    )
    category = django_filters.NumberFilter(
        field_name="subcategory__category_id"
    )
    subcategory = django_filters.NumberFilter(
        field_name="subcategory_id"
    )
    featured = django_filters.BooleanFilter(
        field_name="is_featured"
    )
    active = django_filters.BooleanFilter(
        field_name="is_active"
    )
    in_stock = django_filters.BooleanFilter(
        method="filter_in_stock"
    )
    min_price = django_filters.NumberFilter(
        field_name="price",
        lookup_expr="gte"
    )
    max_price = django_filters.NumberFilter(
        field_name="price",
        lookup_expr="lte"
    )
    on_sale = django_filters.BooleanFilter(
        method="filter_on_sale"
    )

    def filter_search(self, queryset, name, value):
        value=value.strip()
        if not value:
            return queryset
        return queryset.filter(
            models.Q(name__icontains=value) |
            models.Q(reference__icontains=value) |
            models.Q(description__icontains=value) |
            models.Q(composition__icontains=value) |
            models.Q(usage__icontains=value) |
            models.Q(subcategory__name__icontains=value) |
            models.Q(subcategory__category__name__icontains=value) |
            models.Q(product_range__name__icontains=value)
        ).distinct()

    def filter_in_stock(self, queryset, name, value):
        if value:
            return queryset.filter(stock__gt=0)
        return queryset

    def filter_on_sale(self, queryset, name, value):
        if value:
            return queryset.filter(
                promotional_price__isnull=False,
                promotional_price__lt=models.F("price")
            )
        return queryset

    class Meta:
        model=Product
        fields=[
            "search",
            "category",
            "subcategory",
            "featured",
            "active",
            "in_stock",
            "min_price",
            "max_price",
            "on_sale",
        ]