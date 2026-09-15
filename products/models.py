from django.db import models
from django.core.validators import MinValueValidator
from django.utils.text import slugify


def generate_unique_slug(instance, value, slug_field="slug"):
    base_slug = slugify(value)

    if not base_slug:
        base_slug = "element"

    slug = base_slug
    model_class = instance.__class__
    counter = 2

    while model_class.objects.filter(
        **{slug_field: slug}
    ).exclude(pk=instance.pk).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1

    return slug


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, null=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="categories/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self, self.name)

        super().save(*args, **kwargs)


class SubCategory(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="subcategories"
    )
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=60, blank=True,null=True)
    description = models.TextField(blank=True)
    image = models.ImageField(
        upload_to="subcategories/",
        blank=True,
        null=True
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Sous-catégorie"
        verbose_name_plural = "Sous-catégories"
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["category", "name"],
                name="unique_subcategory_per_category"
            ),
            models.UniqueConstraint(
                fields=["category", "slug"],
                name="unique_subcategory_slug_per_category"
            )
        ]

    def __str__(self):
        return f"{self.category.name} - {self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)

            if not base_slug:
                base_slug = "sous-categorie"

            slug = base_slug
            counter = 2

            while SubCategory.objects.filter(
                category=self.category,
                slug=slug
            ).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)


class ProductRange(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, null=True, blank=True)
    description = models.TextField(blank=True)

    price = models.DecimalField(
        max_digits=12,
        null=True,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    image = models.ImageField(
        upload_to="product_ranges/",
        blank=True,
        null=True
    )

    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Gamme de produits"
        verbose_name_plural = "Gammes de produits"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self, self.name)

        super().save(*args, **kwargs)


class Product(models.Model):
    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.PROTECT,
        related_name="products"
    )
    product_range = models.ForeignKey(
        ProductRange,
        on_delete=models.SET_NULL,
        related_name="products",
        blank=True,
        null=True
    )
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=60, null=True, blank=True)
    reference = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    composition = models.TextField(blank=True)
    usage = models.TextField(blank=True)
    precautions = models.TextField(blank=True)
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    promotional_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0)]
    )
    stock = models.PositiveIntegerField(default=0)
    main_image = models.ImageField(
        upload_to="products/",
        blank=True,
        null=True
    )
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self, self.name)

        super().save(*args, **kwargs)

    @property
    def current_price(self):
        if (
            self.promotional_price is not None
            and self.promotional_price < self.price
        ):
            return self.promotional_price

        return self.price

    @property
    def is_on_sale(self):
        return (
            self.promotional_price is not None
            and self.promotional_price < self.price
        )


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(
        upload_to="products/gallery/"
    )
    alt_text = models.CharField(
        max_length=50,
        blank=True
    )
    is_primary = models.BooleanField(
        default=False
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = "Image du produit"
        verbose_name_plural = "Images des produits"
        ordering = ["-is_primary", "-created_at"]

    def __str__(self):
        return f"Image - {self.product.name}"