from django.conf import settings
from django.db import models
from products.models import Product, ProductRange

class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cart"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Panier"
        verbose_name_plural = "Paniers"

    def __str__(self):
        return f"Panier de {self.user.email}"

    @property
    def total_items(self):
        return sum(
            item.quantity
            for item in self.items.all()
        )

    @property
    def subtotal(self):
        return sum(
            item.subtotal
            for item in self.items.all()
        )


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="cart_items",
        null=True,
        blank=True
    )

    product_range = models.ForeignKey(
        ProductRange,
        on_delete=models.CASCADE,
        related_name="cart_items",
        null=True,
        blank=True
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "Article du panier"
        verbose_name_plural = "Articles du panier"
        constraints = [
            models.UniqueConstraint(
                fields=["cart", "product"],
                condition=models.Q(product__isnull=False),
                name="unique_cart_product"
            ),
            models.UniqueConstraint(
                fields=["cart", "product_range"],
                condition=models.Q(product_range__isnull=False),
                name="unique_cart_product_range"
            ),
            models.CheckConstraint(
                condition=(
                    models.Q(product__isnull=False, product_range__isnull=True) |
                    models.Q(product__isnull=True, product_range__isnull=False)
                ),
                name="cart_item_one_type_only"
            )
        ]

    def __str__(self):
        if self.product is not None:
            return f"{self.product.name} x {self.quantity}"

        if self.product_range is not None:
            return f"{self.product_range.name} x {self.quantity}"

        return f"Article panier #{self.id}"

    @property
    def item_type(self):
        if self.product_range is not None:
            return "range"

        return "product"

    @property
    def item_name(self):
        if self.product_range is not None:
            return self.product_range.name

        if self.product is not None:
            return self.product.name

        return "Article"

    @property
    def unit_price(self):
        if self.product_range is not None:
            if hasattr(self.product_range, "current_price"):
                return self.product_range.current_price

            if hasattr(self.product_range, "promotional_price"):
                return self.product_range.promotional_price

            if hasattr(self.product_range, "price"):
                return self.product_range.price

            return 0

        if self.product is not None:
            return self.product.current_price

        return 0

    @property
    def subtotal(self):
        return self.unit_price * self.quantity