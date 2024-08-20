from django.contrib import admin
from .models import OrderPlaced, Product, Customer, Cart, Payment

# Register Product model
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'selling_price', 'discounted_price', 'category', 'product_image')
    search_fields = ('title', 'category')
    list_filter = ('category',)

# Register Customer model
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'city', 'state', 'mobile')
    search_fields = ('name', 'user__username')
    list_filter = ('state',)

# Register Cart model
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'total_cost')
    search_fields = ('user__username', 'product__title')
    readonly_fields = ('total_cost',)

# Register Payment model
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'paypal_order_id', 'paypal_payment_status', 'paid')
    search_fields = ('paypal_order_id', 'paypal_payment_id')
    list_filter = ('paid',)

# Register OrderPlaced model
@admin.register(OrderPlaced)
class OrderPlacedAdmin(admin.ModelAdmin):
    list_display = ('user', 'customer', 'product', 'quantity', 'ordered_date', 'payment_id')
    search_fields = ('user__username', 'customer__name', 'product__title', 'payment_id')
    list_filter = ('ordered_date', 'user', 'customer', 'product')
    ordering = ('-ordered_date',)
