# Register your models here.
from django.contrib import admin
from .models import Product, Category, Size, Color, Banner, SubCategory


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'category', 'gender', 'type', 'created_at')
    list_filter = ('category', 'gender', 'type')
    search_fields = ('title',)


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title',)


admin.site.register(Size)
admin.site.register(Category)
admin.site.register(Color)
admin.site.register(SubCategory)
