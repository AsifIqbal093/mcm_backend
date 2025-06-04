from django.db import models

class Brand(models.Model):
    id = models.AutoField(primary_key=True)
    brand_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.brand_name

class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=False, blank=True, null=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=False)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    sub_categories = models.ManyToManyField('SubCategory', related_name='categories', blank=True, null=True)


    def __str__(self):
        return self.name

    
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=100, unique=True, null=True, blank=True)
    reference = models.CharField(max_length=100, unique=True, null=True, blank=True)
    regular_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sale_quantity = models.PositiveIntegerField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    sold_items = models.PositiveIntegerField(default=0)
    product_summary = models.TextField(blank=True, null=True)
    product_description = models.TextField(blank=True, null=True)
    product_thumbnail = models.ImageField(upload_to='products/thumbnails/', null=True, blank=True)
    product_video = models.FileField(upload_to='products/videos/', null=True, blank=True)
    SKU = models.CharField(max_length=100, unique=True , default='sku')
    stock = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=100, default='active')

    # Updated ForeignKeys
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True, related_name='associated_brand')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name='associated_category')

    def __str__(self):
        return self.product_name

class ProductGallery(models.Model):
    product = models.ForeignKey(Product, related_name='gallery', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_gallery/')

    def __str__(self):
        return f"Gallery Image for {self.product.product_name}"