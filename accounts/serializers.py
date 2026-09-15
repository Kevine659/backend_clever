from rest_framework import serializers
from .models import User
from orders.models import Order, OrderItem
from products.models import Product, ProductRange

class ProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    orders_count = serializers.SerializerMethodField()
    total_spent = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "phone",
            "address",
            "city",
            "date_joined",
            "updated_at",
            "orders_count",
            "total_spent",
        ]
        read_only_fields = [
            "id",
            "email",
            "full_name",
            "date_joined",
            "updated_at",
            "orders_count",
            "total_spent",
        ]

    def get_orders_count(self, obj):
        return obj.orders.count()

    def get_total_spent(self, obj):
        total = sum(
            order.total_amount
            for order in obj.orders.exclude(status="cancelled")
        )
        return total


class OrderItemSerializer(serializers.ModelSerializer):
    product_id = serializers.SerializerMethodField()
    product_image = serializers.SerializerMethodField()
    product_slug = serializers.SerializerMethodField()
    item_type = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "item_type",
            "product_id",
            "product_name",
            "product_image",
            "product_slug",
            "quantity",
            "price",
            "subtotal",
        ]

    def get_product_id(self, obj):
        if obj.product:
            return obj.product.id
        if obj.product_range:
            return obj.product_range.id
        return None

    def get_product_image(self, obj):
        request = self.context.get("request")

        image = None

        if obj.product:
            image = obj.product.main_image

        elif obj.product_range:
            image = obj.product_range.image

        if not image:
            return None

        try:
            url = image.url

            if request:
                return request.build_absolute_uri(url)

            return url

        except Exception:
            return None

    def get_product_slug(self, obj):
        if obj.product:
            return obj.product.slug

        if obj.product_range:
            return obj.product_range.slug

        return ""

    def get_item_type(self, obj):
        if obj.product:
            return "product"

        if obj.product_range:
            return "range"

        return "unknown"


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    status_label = serializers.CharField(
        source="get_status_display",
        read_only=True
    )
    items_count = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "id",
            "first_name",
            "last_name",
            "phone",
            "email",
            "city",
            "address",
            "total_amount",
            "status",
            "status_label",
            "commercial",
            "created_at",
            "updated_at",
            "items_count",
            "items",
        ]

    def get_items_count(self, obj):
        return sum(
            item.quantity
            for item in obj.items.all()
        )