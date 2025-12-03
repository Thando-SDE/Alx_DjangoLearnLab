"""
Views for the API app.
Implements generic views for Book model CRUD operations.
"""
from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer


class BookListView(generics.ListAPIView):
    """
    List view for retrieving all books.
    
    Provides GET method to retrieve a list of all Book instances.
    Uses BookSerializer for data serialization.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Read-only access for all


class BookDetailView(generics.RetrieveAPIView):
    """
    Detail view for retrieving a single book by ID.
    
    Provides GET method to retrieve a specific Book instance by primary key.
    Uses BookSerializer for data serialization.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Read-only access for all


class BookCreateView(generics.CreateAPIView):
    """
    Create view for adding a new book.
    
    Provides POST method to create a new Book instance.
    Uses BookSerializer for data validation and serialization.
    Includes custom validation from BookSerializer.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users


class BookUpdateView(generics.UpdateAPIView):
    """
    Update view for modifying an existing book.
    
    Provides PUT and PATCH methods to update an existing Book instance.
    Uses BookSerializer for data validation and serialization.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users


class BookDeleteView(generics.DestroyAPIView):
    """
    Delete view for removing a book.
    
    Provides DELETE method to remove a Book instance.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users
