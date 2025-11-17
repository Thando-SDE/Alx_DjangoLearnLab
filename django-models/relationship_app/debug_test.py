import os
import sys

print("=== DEBUGGING PATH ISSUE ===")

# Show current directory and files
print(f"Current directory: {os.getcwd()}")
print("Files in current directory:")
for item in os.listdir('.'):
    print(f"  - {item}")

print("\nFiles in LibraryProject:")
for item in os.listdir('LibraryProject'):
    print(f"  - {item}")

# Add current directory to Python path
current_dir = os.getcwd()
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)
    print(f"✓ Added {current_dir} to Python path")

print(f"Python path: {sys.path}")

try:
    os.environ['DJANGO_SETTINGS_MODULE'] = 'LibraryProject.settings'
    import django
    django.setup()
    print("✓ Django setup successful!")
except Exception as e:
    print(f"✗ Error: {e}")
