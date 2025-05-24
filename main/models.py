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

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('shoes', 'Shoes'),
        ('clothes', 'Clothes'),
    ]
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
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

    def __str__(self):
        return self.title

