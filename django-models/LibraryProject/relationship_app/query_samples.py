import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

def query_all_books_by_author(author_name):
    """
    Query all books by a specific author
    """
    try:
        author = Author.objects.get(name=author_name)
        books = author.books.all()
        return books
    except Author.DoesNotExist:
        return []

def list_all_books_in_library(library_name):
    """
    List all books in a library
    """
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        return books
    except Library.DoesNotExist:
        return []

def get_librarian_for_library(library_name):
    """
    Retrieve the librarian for a library
    """
    try:
        library = Library.objects.get(name=library_name)
        librarian = library.librarian
        return librarian
    except Library.DoesNotExist:
        return None
    except Librarian.DoesNotExist:
        return None

# Demonstration code
if __name__ == "__main__":
    # Create sample data for testing
    Author.objects.all().delete()
    Book.objects.all().delete()
    Library.objects.all().delete()
    Librarian.objects.all().delete()
    
    author1 = Author.objects.create(name="J.K. Rowling")
    author2 = Author.objects.create(name="George Orwell")
    
    book1 = Book.objects.create(title="Harry Potter 1", author=author1)
    book2 = Book.objects.create(title="Harry Potter 2", author=author1)
    book3 = Book.objects.create(title="1984", author=author2)
    
    library = Library.objects.create(name="Main Library")
    library.books.add(book1, book2, book3)
    
    Librarian.objects.create(name="Alice", library=library)
    
    # Test the queries
    print("Testing queries:")
    
    # Query all books by a specific author
    books = query_all_books_by_author("J.K. Rowling")
    print(f"Books by J.K. Rowling: {[b.title for b in books]}")
    
    # List all books in a library
    books = list_all_books_in_library("Main Library")
    print(f"Books in Main Library: {[b.title for b in books]}")
    
    # Retrieve the librarian for a library
    librarian = get_librarian_for_library("Main Library")
    print(f"Librarian for Main Library: {librarian.name}")
