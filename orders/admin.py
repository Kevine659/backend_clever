from django.contrib import admin

from .models import (
    Commercial,
    Order,
    OrderItem,
)


@admin.register(Commercial)
class CommercialAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "whatsapp_number",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name",
        "whatsapp_number",
    )


class OrderItemInline(admin.TabularInline):

    model = OrderItem

    extra = 0

    readonly_fields = (
        "product_name",
        "quantity",
        "price",
        "subtotal",
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "first_name",
        "last_name",
        "phone",
        "total_amount",
        "status",
        "commercial",
        "created_at",
    )

    list_filter = (
        "status",
        "commercial",
        "created_at",
    )

    search_fields = (
        "first_name",
        "last_name",
        "phone",
        "email",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    inlines = [
        OrderItemInline
    ]