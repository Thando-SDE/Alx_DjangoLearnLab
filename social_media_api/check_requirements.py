#!/usr/bin/env python3
import os
import sys

print("Checking Task 4 Requirements...")
print("=" * 60)

# Read settings.py
with open('social_media_api/settings.py', 'r') as f:
    settings_content = f.read()

requirements_met = {
    'debug_false': False,
    'security_headers': False,
    'database_config': False,
    'static_files': False,
}

# Check 1: DEBUG = False
print("\n1. Checking DEBUG = False...")
if 'DEBUG = False' in settings_content:
    print("   ✅ DEBUG = False is explicitly set")
    requirements_met['debug_false'] = True
else:
    print("   ❌ DEBUG = False not found")

# Check 2: Security settings
print("\n2. Checking security settings...")
security_settings = [
    'SECURE_BROWSER_XSS_FILTER = True',
    'X_FRAME_OPTIONS = \'DENY\'',
    'SECURE_CONTENT_TYPE_NOSNIFF = True',
    'SECURE_SSL_REDIRECT = True',
]

all_security = True
for setting in security_settings:
    if setting in settings_content:
        print(f"   ✅ {setting}")
    else:
        print(f"   ❌ {setting} missing")
        all_security = False

requirements_met['security_headers'] = all_security

# Check 3: Database configuration
print("\n3. Checking database configuration...")
if 'dj_database_url' in settings_content and 'DATABASE_URL' in settings_content:
    print("   ✅ PostgreSQL configuration with dj-database-url")
    requirements_met['database_config'] = True
else:
    print("   ❌ Database configuration missing")

# Check 4: Static files configuration
print("\n4. Checking static files configuration...")
if 'STATICFILES_STORAGE = \'whitenoise.storage.CompressedManifestStaticFilesStorage\'' in settings_content:
    print("   ✅ WhiteNoise static files storage configured")
    requirements_met['static_files'] = True
else:
    print("   ❌ WhiteNoise configuration missing")

# Check 5: collectstatic setup
print("\n5. Checking collectstatic setup...")
if 'STATIC_ROOT =' in settings_content and 'collectstatic' in settings_content:
    print("   ✅ STATIC_ROOT configured for collectstatic")
else:
    print("   ❌ collectstatic configuration incomplete")

# Summary
print("\n" + "=" * 60)
print("REQUIREMENTS SUMMARY:")
print("=" * 60)

all_passed = True
for req, met in requirements_met.items():
    status = "✅ PASS" if met else "❌ FAIL"
    print(f"{status} - {req.replace('_', ' ').title()}")

if all(requirements_met.values()):
    print("\n🎉 ALL TASK 4 REQUIREMENTS MET!")
else:
    print("\n⚠️  Some requirements not met. Please fix the issues above.")
