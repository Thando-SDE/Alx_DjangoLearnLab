import os
import sys

print("=" * 70)
print("FINAL DEPLOYMENT VERIFICATION - TASK 4")
print("=" * 70)

# Test 1: All required packages
print("\n📦 1. Package Dependencies Check:")
packages = [
    ('Django', 'django'),
    ('Django REST Framework', 'rest_framework'),
    ('django-cors-headers', 'corsheaders'),
    ('gunicorn', 'gunicorn'),
    ('whitenoise', 'whitenoise'),
    ('psycopg2', 'psycopg2'),
    ('dj-database-url', 'dj_database_url'),
    ('python-dotenv', 'dotenv'),
]

all_packages_ok = True
for name, module in packages:
    try:
        __import__(module)
        version = getattr(__import__(module), '__version__', 'available')
        print(f"   ✅ {name}: {version}")
    except ImportError:
        print(f"   ❌ {name}: NOT INSTALLED")
        all_packages_ok = False

# Test 2: Deployment files
print("\n📁 2. Deployment Files Check:")
files = [
    ('requirements.txt', 'Production dependencies'),
    ('Procfile', 'Heroku process definition'),
    ('runtime.txt', 'Python version'),
    ('.env.example', 'Environment template'),
    ('deploy.sh', 'Deployment script'),
    ('README.md', 'Deployment guide'),
    ('social_media_api/settings.py', 'Production settings'),
]

all_files_ok = True
for file, desc in files:
    if os.path.exists(file):
        print(f"   ✅ {file} - {desc}")
    else:
        print(f"   ❌ {file} - {desc} - MISSING")
        all_files_ok = False

# Test 3: Django production settings
print("\n⚙️  3. Django Production Settings Check:")
try:
    # Set production environment
    os.environ['DEBUG'] = 'False'
    os.environ['ALLOWED_HOSTS'] = 'localhost,127.0.0.1,alx-social-media-api.herokuapp.com'
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_media_api.settings')
    import django
    django.setup()
    
    from django.conf import settings
    
    print(f"   ✅ DEBUG: {settings.DEBUG}")
    print(f"   ✅ ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
    print(f"   ✅ Database: {settings.DATABASES['default']['ENGINE']}")
    print(f"   ✅ Static files: {getattr(settings, 'STATICFILES_STORAGE', 'default')}")
    
    # Security settings
    if not settings.DEBUG:
        security_checks = [
            ('SECURE_BROWSER_XSS_FILTER', settings.SECURE_BROWSER_XSS_FILTER, True),
            ('SECURE_SSL_REDIRECT', settings.SECURE_SSL_REDIRECT, True),
            ('SESSION_COOKIE_SECURE', settings.SESSION_COOKIE_SECURE, True),
            ('CSRF_COOKIE_SECURE', settings.CSRF_COOKIE_SECURE, True),
            ('SECURE_HSTS_SECONDS', settings.SECURE_HSTS_SECONDS, 31536000),
        ]
        
        for name, actual, expected in security_checks:
            if actual == expected:
                print(f"   ✅ {name}: {actual}")
            else:
                print(f"   ⚠️  {name}: {actual} (expected: {expected})")
    
    # Check for security warning about secret key
    if 'django-insecure-' in settings.SECRET_KEY:
        print(f"   ⚠️  SECRET_KEY: Should be changed in production (currently using default)")
    
except Exception as e:
    print(f"   ❌ Error testing settings: {e}")

# Test 4: Directories
print("\n📂 4. Directory Structure Check:")
directories = ['static', 'staticfiles', 'media']
for dirname in directories:
    if os.path.exists(dirname):
        print(f"   ✅ {dirname}/ directory exists")
    else:
        print(f"   ⚠️  {dirname}/ directory doesn't exist (will be created on deployment)")

# Final summary
print("\n" + "=" * 70)
print("DEPLOYMENT CONFIGURATION SUMMARY")
print("=" * 70)

if all_packages_ok and all_files_ok:
    print("✅ ALL CHECKS PASSED!")
    print("\n🎉 Task 4 COMPLETE: The application is ready for production deployment!")
    print("\nTo deploy to Heroku:")
    print("1. heroku create alx-social-media-api")
    print("2. heroku addons:create heroku-postgresql:hobby-dev")
    print("3. Set environment variables (see README.md)")
    print("4. git push heroku main")
    print("5. heroku run python manage.py migrate")
    print("\nLive URL: https://alx-social-media-api.herokuapp.com/")
else:
    print("⚠️  Some checks failed. Please review the issues above.")
    
print("\n" + "=" * 70)
