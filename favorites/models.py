import uuid
from django.conf import settings
from django.db import models
from products.models import Product


class Favorite(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="favorites",
        null=True,
        blank=True
    )
    guest_id = models.UUIDField(
        null=True,
        blank=True,
        db_index=True
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="favorites"
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = "Favori"
        verbose_name_plural = "Favoris"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "product"],
                condition=models.Q(user__isnull=False),
                name="unique_user_product_favorite"
            ),
            models.UniqueConstraint(
                fields=["guest_id", "product"],
                condition=models.Q(guest_id__isnull=False),
                name="unique_guest_product_favorite"
            )
        ]

    def __str__(self):
        if self.user:
            return f"{self.user.email} - {self.product.name}"
        return f"Visiteur {self.guest_id} - {self.product.name}"