#!/usr/bin/env python3
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_media_api.settings')

import django
django.setup()

from django.conf import settings

print("Database PORT Configuration Test")
print("=" * 50)

db_config = settings.DATABASES['default']
print(f"Database Engine: {db_config.get('ENGINE')}")
print(f"Database Name: {db_config.get('NAME')}")

# Check PORT
port = db_config.get('PORT', 'NOT SET')
print(f"Database PORT: '{port}'")

if port == '5432':
    print("✅ PORT is explicitly set to '5432' for PostgreSQL")
elif port == '':
    print("✅ PORT is explicitly set to empty string '' for SQLite")
else:
    print(f"⚠️  PORT is set to '{port}'")

print("\nFull database configuration:")
for key, value in db_config.items():
    print(f"  {key}: {value}")
