from django.db import models
from django.conf import settings
from estore.models import Product

class Order(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    ]

    DELIVERY_STATUS_CHOICES = [
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    products = models.ManyToManyField(Product, related_name='orders')
    date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')
    status = models.CharField(max_length=10, choices=DELIVERY_STATUS_CHOICES, default='processing')

    def __str__(self):
        return f"Order #{self.order_id} by {self.user.username}"


class DeliveryInfo(models.Model):
    order = models.OneToOneField('Order', on_delete=models.CASCADE, related_name='delivery_info')
    recipient_name = models.CharField(max_length=255)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"Delivery for Order #{self.order.order_id}"

class OrderProduct(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='order_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        return (self.product.sale_price or 0) * self.quantity


class Banner(models.Model):
    BANNER_POSITIONS = [
        ('slider_1', 'Slider 1'),
        ('slider_2', 'Slider 2'),
        ('slider_3', 'Slider 3'),
        ('top_1', 'Banner Top 1'),
        ('top_2', 'Banner Top 2'),
        ('home_1', 'Banner Home 1'),
        ('home_2', 'Banner Home 2'),
        ('home_3', 'Banner Home 3'),
        ('footer_1', 'Banner Footer 1'),
        ('footer_2', 'Banner Footer 2')
    ]

    image = models.ImageField(upload_to='banners/')
    position = models.CharField(max_length=20, choices=BANNER_POSITIONS)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.position} - {self.id}"
