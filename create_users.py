#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TileCommerce.settings')
django.setup()

from django.contrib.auth.models import User
from shop.models import UserProfile

# Create superuser if it doesn't exist
if not User.objects.filter(username='admin').exists():
    user = User.objects.create_superuser('admin', 'admin@test.com', 'admin123')
    UserProfile.objects.create(user=user)
    print('✓ Superuser created: Username=admin, Password=admin123')
else:
    print('✓ Superuser already exists')

# Create demo user for testing
if not User.objects.filter(username='kazi').exists():
    user = User.objects.create_user(
        username='kazi',
        email='kazi@example.com',
        password='kazi123',
        first_name='Kazi',
        last_name='Mahbub'
    )
    profile = UserProfile.objects.create(
        user=user,
        gender='M',
        phone_number='1234567890',
        country_code='+90'
    )
    print('✓ Demo user created: Username=kazi, Password=kazi123')
else:
    print('✓ Demo user already exists')

print('\n' + '='*60)
print('CREDENTIALS FOR TESTING:')
print('='*60)
print('\nAdmin Panel (Superuser):')
print('  URL: http://127.0.0.1:8000/admin/')
print('  Username: admin')
print('  Password: admin123')
print('\nProfile Page (Demo User):')
print('  URL: http://127.0.0.1:8000/profile/')
print('  Username: kazi')
print('  Password: kazi123')
print('='*60)
