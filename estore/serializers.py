# ---------------- New Model Serializers ---------------- #
from rest_framework import serializers
from .models import *

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'brand_name']


class SubCategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'slug', 'description', 'parent', 'children']

    def get_children(self, obj):
        if obj.children.exists():
            return SubCategorySerializer(obj.children.all(), many=True).data
        return []
    

class CategorySerializer(serializers.ModelSerializer):
    sub_categories = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=SubCategory.objects.all()
    )

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'created_at', 'sub_categories']

    def create(self, validated_data):
        sub_categories = validated_data.pop('sub_categories', [])
        category = Category.objects.create(**validated_data)
        if sub_categories:
            category.sub_categories.set(sub_categories)
        return category

    def update(self, instance, validated_data):
        sub_categories = validated_data.pop('sub_categories', None)

        # update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # update subcategories if provided
        if sub_categories is not None:
            instance.sub_categories.set(sub_categories)

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
