# Register your models here.
from django.contrib import admin
from .models import Product, Category, Size, Color, Banner, SubCategory, MpesaTransaction, Vendor, Sale, Order


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


from django.contrib import admin
from django.contrib import messages
from .models import OrderItem, Product

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'status')
    list_filter = ('status',)

    def save_model(self, request, obj, form, change):
        if change and 'status' in form.changed_data:
            if obj.status == 'completed':
                product = obj.product
                if product.quantity >= obj.quantity:
                    product.quantity -= obj.quantity
                    product.save()
                else:
                    messages.error(request, f"Not enough stock for {product.title}")
                    return  # prevent saving if not enough stock
        super().save_model(request, obj, form, change)

admin.site.register(OrderItem, OrderItemAdmin)


@admin.register(Order)
class Order(admin.ModelAdmin):
    list_display = ('name', 'email', 'status')
    search_fields = ('name', 'email', 'status')
    list_filter = ('name', 'email', 'status')

admin.site.register(Size)
admin.site.register(Category)
admin.site.register(Color)
admin.site.register(SubCategory)
admin.site.register(Vendor)
admin.site.register(Sale)

