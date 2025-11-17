import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book

# Simple test
print("Testing Django setup...")
author = Author.objects.create(name="Test Author")
book = Book.objects.create(title="Test Book", author=author)
print(f"Created: {book.title} by {book.author.name}")
print("✓ Django setup successful!")
