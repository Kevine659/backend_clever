from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    SubCategoryViewSet,
    ProductRangeViewSet,
    ProductViewSet,
)

router = DefaultRouter()

router.register(
    "categories",
    CategoryViewSet,
    basename="categories"
)

router.register(
    "subcategories",
    SubCategoryViewSet,
    basename="subcategories"
)

router.register(
    "product-ranges",
    ProductRangeViewSet,
    basename="product-ranges"
)

router.register(
    "",
    ProductViewSet,
    basename="products"
)

urlpatterns = [
    path("", include(router.urls)),
]