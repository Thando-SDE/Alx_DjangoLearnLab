import os
import sys
import django

# Add current directory to Python path
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

def demonstrate_relationships():
    print("DJANGO ORM RELATIONSHIP DEMONSTRATIONS")
    print("=" * 60)
    print()
    
    # Clean up any existing data
    Author.objects.all().delete()
    Book.objects.all().delete()
    Library.objects.all().delete()
    Librarian.objects.all().delete()
    
    # Create sample data
    print("Creating sample data...")
    
    # Create authors
    author1 = Author.objects.create(name="J.K. Rowling")
    author2 = Author.objects.create(name="George Orwell")
    author3 = Author.objects.create(name="Agatha Christie")
    
    # Create books
    book1 = Book.objects.create(title="Harry Potter and the Philosopher's Stone", author=author1)
    book2 = Book.objects.create(title="Harry Potter and the Chamber of Secrets", author=author1)
    book3 = Book.objects.create(title="1984", author=author2)
    book4 = Book.objects.create(title="Animal Farm", author=author2)
    book5 = Book.objects.create(title="Murder on the Orient Express", author=author3)
    
    # Create libraries
    central_library = Library.objects.create(name="Central Public Library")
    city_library = Library.objects.create(name="City Library")
    
    # Add books to libraries
    central_library.books.add(book1, book2, book3, book4, book5)
    city_library.books.add(book1, book3, book5)
    
    # Create librarians
    Librarian.objects.create(name="Alice Johnson", library=central_library)
    Librarian.objects.create(name="Bob Smith", library=city_library)
    
    print("Sample data created successfully!")
    print()
    
    # 1. ForeignKey: Query all books by a specific author
    print("1. QUERY ALL BOOKS BY A SPECIFIC AUTHOR (ForeignKey)")
    print("=" * 50)
    author = Author.objects.get(name="J.K. Rowling")
    books = author.books.all()
    print(f"All books by {author.name}:")
    for book in books:
        print(f"  - {book.title}")
    print(f"Total: {books.count()} books")
    print()
    
    # 2. ManyToMany: List all books in a library
    print("2. LIST ALL BOOKS IN A LIBRARY (ManyToMany)")
    print("=" * 50)
    library = Library.objects.get(name="Central Public Library")
    books = library.books.all()
    print(f"All books in {library.name}:")
    for book in books:
        print(f"  - {book.title} by {book.author.name}")
    print(f"Total: {books.count()} books")
    print()
    
    # 3. OneToOne: Retrieve the librarian for a library
    print("3. RETRIEVE THE LIBRARIAN FOR A LIBRARY (OneToOne)")
    print("=" * 50)
    library = Library.objects.get(name="Central Public Library")
    librarian = library.librarian
    print(f"Librarian for {library.name}: {librarian.name}")
    print()
    
    print("✓ All Django ORM relationship demonstrations completed successfully!")

if __name__ == "__main__":
    demonstrate_relationships()
