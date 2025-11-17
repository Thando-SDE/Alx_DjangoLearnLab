import os
import sys
import django

# Add current directory to Python path
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')

try:
    django.setup()
    print("✓ Django setup successful!")
    
    from relationship_app.models import Author, Book, Library, Librarian
    
    # Test creating objects
    print("Creating sample data...")
    
    author1 = Author.objects.create(name="J.K. Rowling")
    author2 = Author.objects.create(name="George Orwell")
    
    book1 = Book.objects.create(title="Harry Potter 1", author=author1)
    book2 = Book.objects.create(title="Harry Potter 2", author=author1)
    book3 = Book.objects.create(title="1984", author=author2)
    
    library = Library.objects.create(name="Main Library")
    library.books.add(book1, book2, book3)
    
    librarian = Librarian.objects.create(name="Alice", library=library)
    
    print("✓ Sample data created successfully!")
    print(f"Author: {author1.name}")
    print(f"Books: {[b.title for b in author1.books.all()]}")
    print(f"Library books: {[b.title for b in library.books.all()]}")
    print(f"Librarian: {librarian.name}")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
