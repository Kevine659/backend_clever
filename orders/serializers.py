from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    item_type = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product_name",
            "quantity",
            "price",
            "subtotal",
            "product",
            "product_range",
            "item_type",
            "image",
        ]

    def get_item_type(self, obj):
        if obj.product_range:
            return "range"
        return "product"

    def get_image(self, obj):
        request = self.context.get("request")

        image_field = None

        if obj.product:
            image_field = obj.product.main_image

        elif obj.product_range:
            image_field = obj.product_range.image

        if not image_field:
            return None

        try:
            url = image_field.url

            if request:
                return request.build_absolute_uri(url)

            return url

        except Exception:
            return None


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
            "items",
            "items_count",
        ]

    def get_items_count(self, obj):
        return sum(
            item.quantity
            for item in obj.items.all()
        )