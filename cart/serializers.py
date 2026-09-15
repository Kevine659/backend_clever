from rest_framework import serializers
from .models import Cart, CartItem

class CartItemSerializer(serializers.ModelSerializer):
    item_type = serializers.CharField(
        read_only=True
    )

    product_name = serializers.SerializerMethodField()
    product_reference = serializers.SerializerMethodField()
    product_image = serializers.SerializerMethodField()
    product_range_name = serializers.SerializerMethodField()
    product_range_image = serializers.SerializerMethodField()
    stock = serializers.SerializerMethodField()

    unit_price = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        read_only=True
    )

    subtotal = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        read_only=True
    )

    class Meta:
        model = CartItem
        fields = [
            "id",
            "item_type",
            "product",
            "product_range",
            "product_name",
            "product_reference",
            "product_image",
            "product_range_name",
            "product_range_image",
            "quantity",
            "stock",
            "unit_price",
            "subtotal",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "item_type",
            "product_name",
            "product_reference",
            "product_image",
            "product_range_name",
            "product_range_image",
            "stock",
            "unit_price",
            "subtotal",
            "created_at",
            "updated_at",
        ]

    def get_product_name(self, obj):
        if obj.product:
            return obj.product.name
        return None

    def get_product_reference(self, obj):
        if obj.product:
            return obj.product.reference
        return None

    def get_product_image(self, obj):
        if obj.product and obj.product.main_image:
            return obj.product.main_image.url
        return None

    def get_product_range_name(self, obj):
        if obj.product_range:
            return obj.product_range.name
        return None

    def get_product_range_image(self, obj):
        if obj.product_range and obj.product_range.image:
            return obj.product_range.image.url
        return None

    def get_stock(self, obj):
        if obj.product:
            return obj.product.stock

        if obj.product_range:
            return None

        return 0


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(
        many=True,
        read_only=True
    )

    total_items = serializers.IntegerField(
        read_only=True
    )

    subtotal = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        read_only=True
    )

    class Meta:
        model = Cart
        fields = [
            "id",
            "items",
            "total_items",
            "subtotal",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "items",
            "total_items",
            "subtotal",
            "created_at",
            "updated_at",
        ]


class SyncCartItemSerializer(serializers.Serializer):
    type = serializers.ChoiceField(
        choices=[
            "product",
            "range"
        ]
    )

    product = serializers.IntegerField(
        required=False,
        allow_null=True
    )

    product_range = serializers.IntegerField(
        required=False,
        allow_null=True
    )

    quantity = serializers.IntegerField(
        min_value=1
    )

    def validate(self, attrs):
        item_type = attrs.get("type")
        product = attrs.get("product")
        product_range = attrs.get("product_range")

        if item_type == "product":
            if not product:
                raise serializers.ValidationError({
                    "product": "Le produit est obligatoire."
                })

            attrs["product_range"] = None

        elif item_type == "range":
            if not product_range:
                raise serializers.ValidationError({
                    "product_range": "La gamme est obligatoire."
                })

            attrs["product"] = None

        return attrs