#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TileCommerce.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from django.contrib.auth.models import User
from shop.models import UserProfile

# Find duplicate emails
email_counts = {}
for user in User.objects.all():
    if user.email:
        if user.email not in email_counts:
            email_counts[user.email] = []
        email_counts[user.email].append(user)

# Show and remove duplicates
duplicates = {email: users for email, users in email_counts.items() if len(users) > 1}
if duplicates:
    print("Found duplicate emails:")
    for email, users in duplicates.items():
        print(f"\n{email}:")
        
        # Sort by date_joined to keep the oldest one
        users_sorted = sorted(users, key=lambda u: u.date_joined)
        
        for i, user in enumerate(users_sorted):
            status = "KEEP" if i == 0 else "DELETE"
            print(f"  - [{status}] ID: {user.id}, username: {user.username}, created: {user.date_joined}")
        
        # Delete duplicates (keep the oldest)
        for user in users_sorted[1:]:
            print(f"\n  Deleting user: {user.username} (ID: {user.id})")
            user.delete()
    
    print("\n✓ Cleanup completed!")
else:
    print("✓ No duplicate emails found")

# Show all users
print("\n=== All Users ===")
for user in User.objects.all():
    print(f"ID: {user.id}, username: {user.username}, email: {user.email}")
