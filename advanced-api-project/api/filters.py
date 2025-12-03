"""
Filter sets for API views.
Implements filtering capabilities for Book model.
"""
import django_filters
from .models import Book


class BookFilter(django_filters.FilterSet):
    """
    Filter set for Book model.
    Allows filtering by various attributes like title, author, and publication_year.
    
    Examples:
    - /api/books/?title=Harry Potter (exact match)
    - /api/books/?title__icontains=potter (case-insensitive partial match)
    - /api/books/?author__name=Rowling (filter by author name)
    - /api/books/?publication_year=1997 (exact year)
    - /api/books/?publication_year__gt=1990 (year greater than 1990)
    - /api/books/?publication_year__lt=2000 (year less than 2000)
    """
    title = django_filters.CharFilter(lookup_expr='icontains')
    author__name = django_filters.CharFilter(lookup_expr='icontains')
    publication_year = django_filters.NumberFilter()
    publication_year__gt = django_filters.NumberFilter(field_name='publication_year', lookup_expr='gt')
    publication_year__lt = django_filters.NumberFilter(field_name='publication_year', lookup_expr='lt')
    
    class Meta:
        model = Book
        fields = ['title', 'author__name', 'publication_year']
