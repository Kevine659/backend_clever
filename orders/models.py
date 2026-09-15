from django.conf import settings
from django.db import models
from products.models import Product, ProductRange

class Commercial(models.Model):
    name = models.CharField(max_length=100)
    whatsapp_number = models.CharField(max_length=30, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = "Commercial"
        verbose_name_plural = "Commerciaux"
        ordering = ["id"]
    def __str__(self):
        return f"{self.name} - {self.whatsapp_number}"

class CommercialRotation(models.Model):
    current_index = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = "Rotation commerciale"
        verbose_name_plural = "Rotation commerciale"
    def __str__(self):
        return f"Rotation commerciale (index actuel : {self.current_index})"

class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "En attente"),
        ("confirmed", "Confirmée"),
        ("processing", "En préparation"),
        ("shipped", "Expédiée"),
        ("delivered", "Livrée"),
        ("cancelled", "Annulée"),
    ]
    user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name="orders"
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=30)
    email = models.EmailField(max_length=191)
    city = models.CharField(max_length=100)
    address = models.TextField()
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    commercial = models.ForeignKey(
        Commercial,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"
        ordering = ["-created_at"]
        
    def __str__(self):
        if self.user:
            return f"Commande #{self.id} - {self.user.email}"
        return f"Commande #{self.id} - {self.first_name} {self.last_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="order_items"
    )
    product_range = models.ForeignKey(
        ProductRange,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="order_items"
    )
    product_name = models.CharField(max_length=191)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    class Meta:
        verbose_name = "Article de commande"
        verbose_name_plural = "Articles de commande"
        constraints = [
            models.CheckConstraint(
                condition=(
                    models.Q(product__isnull=False, product_range__isnull=True) |
                    models.Q(product__isnull=True, product_range__isnull=False)
                ),
                name="order_item_one_type_only"
            )
        ]
    def __str__(self):
        return f"{self.product_name} x {self.quantity}"