# ---------------- New Model Serializers ---------------- #
from rest_framework import serializers
from .models import Product, Category, SubCategory, Brand, Inventory

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


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ['id', 'SKU', 'stock', 'status']

class ProductSerializer(serializers.ModelSerializer):
    # These fields will accept only valid primary keys (like a dropdown/choice)
    brand = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all())
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    # Optional: include subcategory and inventory as nested objects for read-only
    inventory = InventorySerializer(read_only=True)

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
            'product_video',
            'brand',
            'category',
            'inventory',
        ]