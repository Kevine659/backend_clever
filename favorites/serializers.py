from rest_framework import serializers
from .models import Favorite


class FavoriteSerializer(serializers.ModelSerializer):

    product_name = serializers.CharField(
        source="product.name",
        read_only=True
    )

    product_price = serializers.DecimalField(
        source="product.current_price",
        max_digits=12,
        decimal_places=2,
        read_only=True
    )

    product_image = serializers.ImageField(
        source="product.main_image",
        read_only=True
    )

    class Meta:
        model = Favorite

        fields = [
            "id",
            "product",
            "product_name",
            "product_price",
            "product_image",
            "created_at"
        ]

        read_only_fields = [
            "id",
            "product_name",
            "product_price",
            "product_image",
            "created_at"
        ]