# ---------------- New Model Serializers ---------------- #
from rest_framework import serializers
from .models import Product,ProductGallery, Category, SubCategory, Brand

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'brand_name']


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'name']

class CategorySerializer(serializers.ModelSerializer):
    sub_categories = SubCategorySerializer(many=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'created_at', 'sub_categories']

    def create(self, validated_data):
        sub_categories_data = validated_data.pop('sub_categories')
        category = Category.objects.create(**validated_data)
        for sub_category_data in sub_categories_data:
            sub_category = SubCategory.objects.create(**sub_category_data)
            category.sub_categories.add(sub_category)
        return category
    
    def update(self, instance, validated_data):
        sub_categories_data = validated_data.pop('sub_categories', [])

        # Update category fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Optional: clear and re-add subcategories
        instance.sub_categories.clear()
        for sub_category_data in sub_categories_data:
            sub_category, _ = SubCategory.objects.get_or_create(**sub_category_data)
            instance.sub_categories.add(sub_category)

        return instance

class ProductGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductGallery
        fields = ['id', 'image']

class ProductSerializer(serializers.ModelSerializer):
    product_thumbnail = serializers.ImageField(required=False)
    gallery = ProductGallerySerializer(many=True, required=False, read_only=True)
    product_gallery = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Product
        fields = [
            'id',
            'product_name',
            'reference',
            'regular_price',
            'sale_price',
            'sale_quantity',
            'date',
            'sold_items',
            'product_summary',
            'product_description',
            'product_thumbnail',
            'product_gallery',
            'gallery',
            'product_video',
            'brand',
            'category',
            'stock',
            'SKU',
            'status',
        ]

    def create(self, validated_data):
        gallery_images = validated_data.pop("product_gallery", [])
        product = Product.objects.create(**validated_data)

        for image in gallery_images:
            ProductGallery.objects.create(product=product, image=image)

        return product
