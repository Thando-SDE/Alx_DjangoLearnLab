import os
import django

# Set the settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'LibraryProject.settings'

try:
    django.setup()
    print("✓ Django setup successful!")
    
    from relationship_app.models import Author, Book
    
    # Test creating objects
    author = Author(name="Test Author")
    author.save()
    
    book = Book(title="Test Book", author=author)
    book.save()
    
    print(f"✓ Created: {book.title} by {book.author.name}")
    print("✓ All tests passed!")
    
except Exception as e:
    print(f"✗ Error: {e}")
