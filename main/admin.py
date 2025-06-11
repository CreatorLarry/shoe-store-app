# Register your models here.
from django.contrib import admin
from .models import Product, Category, Size, Color, Banner, SubCategory, MpesaTransaction, Vendor


admin.site.site_header = "Thread & Trend Admin"
admin.site.site_title = "Thread & Trend Admin"


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


@admin.register(MpesaTransaction)
class MpesaTransactionAdmin(admin.ModelAdmin):
    list_display = ('mpesa_receipt_number', 'phone_number', 'amount', 'result_code', 'transaction_date')
    search_fields = ('mpesa_receipt_number', 'phone_number')
    list_filter = ('result_code', 'transaction_date')


admin.site.register(Size)
admin.site.register(Category)
admin.site.register(Color)
admin.site.register(SubCategory)
admin.site.register(Vendor)

