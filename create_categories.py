import os
import django
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TileCommerce.settings')
django.setup()

from shop.models import Category

categories_to_create = [
    'Floor Tiles',
    'Vitrified Tiles',
    'Wall Tiles',
    'Mosaic Tiles',
    'Bathroom Tiles',
    'Kitchen Tiles',
    'Living Room Tiles',
    'Outdoor Tiles',
    'Parking Tiles',
    'Stone and Brick Cladding',
    'Ceramic Tiles',
    'Tile Accessories'
]

print("Creating categories...\n")
for cat_name in categories_to_create:
    category, created = Category.objects.get_or_create(
        name=cat_name,
        defaults={'slug': slugify(cat_name)}
    )
    if created:
        print(f'✓ Created: {cat_name}')
    else:
        print(f'- Already exists: {cat_name}')

print(f'\n✓ Total categories in database: {Category.objects.count()}')
