# Register your models here.
from django.contrib import admin
from .models import Product, Category, Size, Color


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'category', 'gender', 'type', 'created_at')
    list_filter = ('category', 'gender', 'type')
    search_fields = ('title',)

admin.site.register(Size)
admin.site.register(Category)
admin.site.register(Color)
