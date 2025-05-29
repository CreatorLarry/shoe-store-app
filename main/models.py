from django.db import models
from django.utils.text import slugify


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='categories/', null=True, blank=False)
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=50)
    bootstrap_class = models.CharField(max_length=50, default='secondary')  # For label color

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=100)
    display_image = models.ImageField(upload_to='products/subcategories/', null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.category.name})"


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('shoes', 'Shoes'),
        ('clothes', 'Clothes'),
    ]
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255)
    display_image = models.ImageField(upload_to='products/')
    image_one = models.ImageField(upload_to='products/', null=True, blank=True)
    image_two = models.ImageField(upload_to='products/', null=True, blank=True)
    image_three = models.ImageField(upload_to='products/', null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(blank=True)
    gender = models.CharField(max_length=20, choices=[
        ('men', 'Men'),
        ('women', 'Women'),
        ('children', 'Children'),
        ('unisex', 'Unisex')
    ])
    type = models.CharField(max_length=100)  # e.g. Sneakers, Loafers
    created_at = models.DateTimeField(auto_now_add=True)
    sizes = models.ManyToManyField(Size)
    colors = models.ManyToManyField(Color, blank=True)
    is_new = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Order(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    payment_method = models.CharField(max_length=20)
    items = models.JSONField()  # Store cart items
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.name}"


class Banner(models.Model):
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='banners/')
    link = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

