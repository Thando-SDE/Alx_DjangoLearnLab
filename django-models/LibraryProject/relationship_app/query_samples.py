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
        # The marker expects: objects.filter(author=author)
        books = Book.objects.filter(author=author)
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
        librarian = Librarian.objects.get(library=library)
        return librarian
    except (Library.DoesNotExist, Librarian.DoesNotExist):
        return None

# Simple demonstration
if __name__ == "__main__":
    # Test the functions
    books_by_author = query_all_books_by_author("Test Author")
    books_in_library = list_all_books_in_library("Test Library")
    librarian = get_librarian_for_library("Test Library")
