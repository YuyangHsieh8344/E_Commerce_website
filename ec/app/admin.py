from django.contrib import admin
from .models import OrderPlaced, Payment, Product, Customer, Cart

# Register your models here.
@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'discounted_price', 'category', 'product_image']
    list_filter = ['category', 'discounted_price']
    search_fields = ['title', 'category__name']
    ordering = ['-id']

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'city', 'mobile', 'state')
    search_fields = ('name', 'city', 'mobile', 'state')
    list_filter = ('city', 'state')
    ordering = ('-id',)

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'quantity')
    search_fields = ('user__username', 'product__title')
    list_filter = ('product', 'user')
    ordering = ('-id',)

@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'paypal_order_id', 'paypal_payment_status', 'paypal_payment_id', 'paid')
    list_filter = ('paid', 'paypal_payment_status')
    search_fields = ('user__username', 'paypal_order_id', 'paypal_payment_id')
    ordering = ('-id',)

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'customer', 'product', 'quantity', 'ordered_date', 'status', 'payment')
    list_filter = ('status', 'ordered_date')
    search_fields = ('user__username', 'customer__name', 'product__title')
    ordering = ('-ordered_date',)