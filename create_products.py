import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TileCommerce.settings')
django.setup()

from shop.models import Product, Category
from decimal import Decimal

products_data = [
    {
        'name': 'Premium Ceramic Floor Tile',
        'description': 'High-quality ceramic floor tile with a glossy finish. Perfect for modern living spaces.',
        'price': Decimal('49.99'),
        'category': 'Floor Tiles'
    },
    {
        'name': 'Classic Vitrified Tile',
        'description': 'Durable vitrified tile ideal for kitchens and bathrooms. Water-resistant and easy to clean.',
        'price': Decimal('59.99'),
        'category': 'Vitrified Tiles'
    },
    {
        'name': 'Elegant Wall Tile',
        'description': 'Modern design wall tile for bathroom and kitchen backsplashes. Available in multiple colors.',
        'price': Decimal('39.99'),
        'category': 'Wall Tiles'
    },
    {
        'name': 'Mosaic Decorative Tile',
        'description': 'Beautiful mosaic tiles for accent walls and artistic installations.',
        'price': Decimal('69.99'),
        'category': 'Mosaic Tiles'
    },
    {
        'name': 'Bathroom Floor Tile',
        'description': 'Slip-resistant bathroom floor tile with superior grip and durability.',
        'price': Decimal('54.99'),
        'category': 'Bathroom Tiles'
    },
    {
        'name': 'Kitchen Backsplash Tile',
        'description': 'Stylish kitchen backsplash tile that complements modern kitchen designs.',
        'price': Decimal('44.99'),
        'category': 'Kitchen Tiles'
    },
    {
        'name': 'Living Room Feature Tile',
        'description': 'Premium feature tile for accent walls in living spaces.',
        'price': Decimal('74.99'),
        'category': 'Living Room Tiles'
    },
    {
        'name': 'Outdoor Patio Tile',
        'description': 'Weather-resistant outdoor tile perfect for patios and decks.',
        'price': Decimal('79.99'),
        'category': 'Outdoor Tiles'
    },
    {
        'name': 'Parking Area Tile',
        'description': 'Heavy-duty tile designed for parking areas and commercial spaces.',
        'price': Decimal('89.99'),
        'category': 'Parking Tiles'
    },
    {
        'name': 'Stone Look Tile',
        'description': 'Realistic stone look tile from our premium stone cladding collection.',
        'price': Decimal('99.99'),
        'category': 'Stone and Brick Cladding'
    },
    {
        'name': 'Marble Effect Ceramic',
        'description': 'Beautiful marble effect ceramic tile for elegant interiors.',
        'price': Decimal('64.99'),
        'category': 'Ceramic Tiles'
    },
    {
        'name': 'Tile Grout - White',
        'description': 'Premium white grout for tile installation and repairs.',
        'price': Decimal('24.99'),
        'category': 'Tile Accessories'
    },
    {
        'name': 'Terracotta Tile',
        'description': 'Rustic terracotta tile with authentic aged appearance.',
        'price': Decimal('84.99'),
        'category': 'Floor Tiles'
    },
    {
        'name': 'Porcelain Tile',
        'description': 'Premium porcelain tile for both indoor and outdoor applications.',
        'price': Decimal('94.99'),
        'category': 'Ceramic Tiles'
    },
    {
        'name': 'Hexagonal Mosaic',
        'description': 'Trendy hexagonal mosaic tile for modern interior designs.',
        'price': Decimal('74.99'),
        'category': 'Mosaic Tiles'
    },
]

print("Creating products...\n")

for product_data in products_data:
    category = Category.objects.get(name=product_data['category'])
    product, created = Product.objects.get_or_create(
        name=product_data['name'],
        defaults={
            'description': product_data['description'],
            'price': product_data['price'],
            'category': category,
        }
    )
    if created:
        print(f'✓ Created: {product.name} (${product.price})')
    else:
        print(f'- Already exists: {product.name}')

print(f'\n✓ Total products in database: {Product.objects.count()}')
