from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Product, Category, Order, OrderItem, Payment

# Restricting access to only admin users
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'SKU', 'price', 'stock', 'category', 'date')
    search_fields = ('name', 'SKU', 'category__name')
    list_filter = ('category', 'date')
    autocomplete_fields = ('category',)
    readonly_fields = ('date',)
    fieldsets = (
        ('Product Info', {
            'fields': ('name', 'SKU', 'category', 'image')
        }),
        ('Pricing and Stock', {
            'fields': ('price', 'stock')
        }),
        ('Timestamps', {
            'fields': ('date',)
        }),
    )

    # Restrict CRUD operations to only admin users
    def has_add_permission(self, request):
        return request.user.is_superuser  # Only superuser can add products

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser  # Only superuser can change products

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser  # Only superuser can delete products

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser  # Only superuser can view products in the admin panel

# Register models to the admin panel
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'parent_category')
    search_fields = ('name',)
    list_filter = ('parent_category',)
    prepopulated_fields = {'slug': ('name',)}  # Automatically fill slug based on name


@admin.register(Product)
class ProductAdminCustom(ProductAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'status', 'active', 'total')
    list_filter = ('status', 'active')  # Filter by status and active status
    search_fields = ('id', 'user__email', 'status')
    list_editable = ('active',)  # Allow editing the 'active' field in the list view
    ordering = ('-created_at',)  # Default ordering by creation date (newest first)
    
    # Display total price of the order
    def total(self, obj):
        return sum(item.price * item.quantity for item in obj.items.all())
    total.short_description = 'Total Price'
    
    fieldsets = (
        ('Order Details', {
            'fields': ('user', 'status', 'active')
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')
    search_fields = ('order__id', 'product__name')
    list_filter = ('order', 'product')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'amount', 'transaction_id', 'payment_date', 'payment_method')
    search_fields = ('order__id', 'transaction_id')
    list_filter = ('payment_date', 'payment_method')
