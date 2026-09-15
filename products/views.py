from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.filters import SearchFilter, OrderingFilter

from django_filters.rest_framework import DjangoFilterBackend

from .models import Category, SubCategory, ProductRange, Product
from .serializers import (
    CategorySerializer,
    SubCategorySerializer,
    ProductRangeSerializer,
    ProductSerializer,
)
from .filters import ProductFilter


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Category.objects.filter(
        is_active=True
    ).order_by("name")

    serializer_class = CategorySerializer

    permission_classes = [
        AllowAny
    ]


class SubCategoryViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = SubCategory.objects.filter(
        is_active=True
    ).select_related(
        "category"
    ).order_by("name")

    serializer_class = SubCategorySerializer

    permission_classes = [
        AllowAny
    ]


class ProductRangeViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = ProductRange.objects.filter(
        is_active=True
    ).prefetch_related(
        "products"
    ).order_by("name")

    serializer_class = ProductRangeSerializer

    permission_classes = [
        AllowAny
    ]

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework import viewsets

from .models import Product
from .serializers import ProductSerializer
from .filters import ProductFilter


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = (
        Product.objects
        .filter(
            is_active=True
        )
        .select_related(
            "subcategory",
            "subcategory__category",
            "product_range"
        )
        .prefetch_related(
            "images"
        )
        .order_by(
            "-created_at"
        )
    )

    serializer_class = ProductSerializer

    permission_classes = [
        AllowAny
    ]

    lookup_field = "slug"

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    ]

    filterset_class = ProductFilter

    search_fields = [
        "name",
        "reference",
        "description",
        "composition",
        "usage",
        "subcategory__name",
        "subcategory__category__name",
        "product_range__name"
    ]

    ordering_fields = [
        "name",
        "price",
        "created_at",
        "stock"
    ]

    ordering = [
        "-created_at"
    ]