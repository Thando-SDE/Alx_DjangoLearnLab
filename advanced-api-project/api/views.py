"""
Views for the API app.
Implements generic views with filtering, searching, and ordering capabilities.
"""
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Book
from .serializers import BookSerializer
from .filters import BookFilter


class BookListView(generics.ListAPIView):
    """
    List view for retrieving all books with filtering, searching, and ordering.
    
    Filtering: Uses DjangoFilterBackend with BookFilter for comprehensive filtering
    Example queries:
    - /api/books/?title=Harry Potter (filter by exact title)
    - /api/books/?author__name=Rowling (filter by author name)
    - /api/books/?publication_year=1997 (filter by publication year)
    - /api/books/?publication_year__gt=1990&publication_year__lt=2000 (year range)
    
    Searching: Uses SearchFilter on title and author name fields
    Example: /api/books/?search=Harry Potter (searches in title and author name)
    
    Ordering: Uses OrderingFilter on title, publication_year, and author name
    Example: /api/books/?ordering=title (ascending by title)
    Example: /api/books/?ordering=-publication_year (descending by year)
    Example: /api/books/?ordering=author__name,title (multiple fields)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    # Filtering, Searching, and Ordering configuration
    filter_backends = [filters.DjangoFilterBackend, SearchFilter, OrderingFilter]
    
    # Filtering: Use custom filter set for advanced filtering options
    filterset_class = BookFilter
    
    # Searching: Define which fields can be searched (text search)
    search_fields = ['title', 'author__name']
    
    # Ordering: Define which fields can be used for ordering results
    ordering_fields = ['title', 'publication_year', 'author__name']
    ordering = ['title']  # Default ordering if none specified


class BookDetailView(generics.RetrieveAPIView):
    """
    Detail view for retrieving a single book by ID.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookCreateView(generics.CreateAPIView):
    """
    Create view for adding a new book.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class BookUpdateView(generics.UpdateAPIView):
    """
    Update view for modifying an existing book.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class BookDeleteView(generics.DestroyAPIView):
    """
    Delete view for removing a book.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
