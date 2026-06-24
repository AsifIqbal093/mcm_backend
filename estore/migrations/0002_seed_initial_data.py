# Generated migration for seed data
from django.db import migrations


def create_initial_brands_and_categories(apps, schema_editor):
    """Create initial brands and categories that will work across all environments"""
    Brand = apps.get_model('estore', 'Brand')
    Category = apps.get_model('estore', 'Category')

    # Create brands
    brands_data = [
        {'brand_name': 'Adidas'},
        {'brand_name': 'Nike'},
        {'brand_name': 'Puma'},
        {'brand_name': 'Reebok'},
    ]

    for brand_data in brands_data:
        Brand.objects.get_or_create(**brand_data)

    # Create categories
    categories_data = [
        {
            'name': 'Footwear',
            'slug': 'footwear',
            'description': 'Sports shoes, sneakers, and athletic footwear'
        },
        {
            'name': 'Clothing',
            'slug': 'clothing',
            'description': 'Sports apparel and athletic clothing'
        },
        {
            'name': 'Accessories',
            'slug': 'accessories',
            'description': 'Sports accessories and equipment'
        },
    ]

    for category_data in categories_data:
        Category.objects.get_or_create(
            name=category_data['name'],
            defaults={
                'slug': category_data['slug'],
                'description': category_data['description']
            }
        )


class Migration(migrations.Migration):
    dependencies = [
        ('estore', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_brands_and_categories),
    ]