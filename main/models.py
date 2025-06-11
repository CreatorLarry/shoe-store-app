from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=255)
    is_premium = models.BooleanField(default=False)
    logo = models.ImageField(upload_to='vendor_logos/', null=True, blank=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.business_name


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
        return f"{self.name}"


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('shoes', 'Shoes'),
        ('clothes', 'Clothes'),
    ]
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='products', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255, unique=True)
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
    items = models.TextField(null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="order_items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True)
    colors = models.ManyToManyField(Color, blank=True)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)


class Banner(models.Model):
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='banners/')
    link = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class MpesaTransaction(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='transactions', null=True, blank=True)
    phone_number = models.CharField(max_length=15)
    mpesa_receipt_number = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateTimeField()
    merchant_request_id = models.CharField(max_length=255)
    checkout_request_id = models.CharField(max_length=255)
    result_code = models.IntegerField()
    result_desc = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.mpesa_receipt_number} - {self.phone_number}"


class Sale(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(default=timezone.now)


class Note(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)