"""
Unit tests for API endpoints.
Tests CRUD operations, filtering, searching, ordering, and permissions.
"""
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Author, Book


class BookAPITestCase(TestCase):
    """
    Test case for Book API endpoints.
    """
    def setUp(self):
        """
        Set up test data and client.
        Creates test authors, books, and users for authentication testing.
        """
        # Create test users
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.admin_user = User.objects.create_superuser(
            username='admin',
            password='adminpass123',
            email='admin@example.com'
        )
        
        # Create test authors
        self.author1 = Author.objects.create(name='J.K. Rowling')
        self.author2 = Author.objects.create(name='George Orwell')
        
        # Create test books
        self.book1 = Book.objects.create(
            title='Harry Potter and the Philosopher\'s Stone',
            publication_year=1997,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title='1984',
            publication_year=1949,
            author=self.author2
        )
        self.book3 = Book.objects.create(
            title='Animal Farm',
            publication_year=1945,
            author=self.author2
        )
        
        # Create API client
        self.client = APIClient()
    
    # ==================== CRUD OPERATION TESTS ====================
    
    def test_get_book_list(self):
        """Test GET /api/books/ returns list of all books."""
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertContains(response, 'Harry Potter')
        self.assertContains(response, '1984')
        self.assertContains(response, 'Animal Farm')
    
    def test_get_book_detail(self):
        """Test GET /api/books/<id>/ returns specific book details."""
        response = self.client.get(f'/api/books/{self.book1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Harry Potter and the Philosopher\'s Stone')
        self.assertEqual(response.data['publication_year'], 1997)
        self.assertEqual(response.data['author'], self.author1.id)
    
    def test_create_book_authenticated(self):
        """Test POST /api/books/create/ with authentication creates book."""
        self.client.force_authenticate(user=self.user)
        
        data = {
            'title': 'New Test Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        response = self.client.post('/api/books/create/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4)
        self.assertEqual(Book.objects.last().title, 'New Test Book')
    
    def test_create_book_unauthenticated(self):
        """Test POST /api/books/create/ without authentication fails."""
        data = {
            'title': 'New Test Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        response = self.client.post('/api/books/create/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_update_book_authenticated(self):
        """Test PUT /api/books/update/<id>/ with authentication updates book."""
        self.client.force_authenticate(user=self.user)
        
        data = {
            'title': 'Updated Title',
            'publication_year': 1998,
            'author': self.author1.id
        }
        response = self.client.put(f'/api/books/update/{self.book1.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Refresh from database
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Title')
        self.assertEqual(self.book1.publication_year, 1998)
    
    def test_delete_book_authenticated(self):
        """Test DELETE /api/books/delete/<id>/ with authentication deletes book."""
        self.client.force_authenticate(user=self.user)
        
        response = self.client.delete(f'/api/books/delete/{self.book1.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 2)
        self.assertFalse(Book.objects.filter(id=self.book1.id).exists())
    
    def test_delete_book_unauthenticated(self):
        """Test DELETE /api/books/delete/<id>/ without authentication fails."""
        response = self.client.delete(f'/api/books/delete/{self.book1.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Book.objects.count(), 3)  # Book still exists
    
    # ==================== FILTERING TESTS ====================
    
    def test_filter_by_title(self):
        """Test filtering books by title."""
        response = self.client.get('/api/books/?title=1984')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], '1984')
    
    def test_filter_by_author_name(self):
        """Test filtering books by author name."""
        response = self.client.get('/api/books/?author__name=George Orwell')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # 1984 and Animal Farm
        titles = [book['title'] for book in response.data]
        self.assertIn('1984', titles)
        self.assertIn('Animal Farm', titles)
    
    def test_filter_by_publication_year(self):
        """Test filtering books by publication year."""
        response = self.client.get('/api/books/?publication_year=1997')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Harry Potter and the Philosopher\'s Stone')
    
    def test_filter_by_publication_year_range(self):
        """Test filtering books by publication year range."""
        response = self.client.get('/api/books/?publication_year__gt=1945&publication_year__lt=1990')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only 1984 (1949)
        self.assertEqual(response.data[0]['title'], '1984')
    
    # ==================== SEARCHING TESTS ====================
    
    def test_search_by_title(self):
        """Test searching books by title text."""
        response = self.client.get('/api/books/?search=Harry')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Harry Potter and the Philosopher\'s Stone')
    
    def test_search_by_author_name(self):
        """Test searching books by author name text."""
        response = self.client.get('/api/books/?search=Orwell')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Both Orwell books
        titles = [book['title'] for book in response.data]
        self.assertIn('1984', titles)
        self.assertIn('Animal Farm', titles)
    
    def test_search_case_insensitive(self):
        """Test searching is case insensitive."""
        response = self.client.get('/api/books/?search=harry potter')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    # ==================== ORDERING TESTS ====================
    
    def test_order_by_title_ascending(self):
        """Test ordering books by title ascending."""
        response = self.client.get('/api/books/?ordering=title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, sorted(titles))  # Should be sorted alphabetically
    
    def test_order_by_title_descending(self):
        """Test ordering books by title descending."""
        response = self.client.get('/api/books/?ordering=-title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, sorted(titles, reverse=True))
    
    def test_order_by_publication_year_ascending(self):
        """Test ordering books by publication year ascending."""
        response = self.client.get('/api/books/?ordering=publication_year')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, sorted(years))
    
    def test_order_by_publication_year_descending(self):
        """Test ordering books by publication year descending."""
        response = self.client.get('/api/books/?ordering=-publication_year')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, sorted(years, reverse=True))
    
    # ==================== VALIDATION TESTS ====================
    
    def test_create_book_future_year_validation(self):
        """Test validation prevents creating book with future publication year."""
        self.client.force_authenticate(user=self.user)
        
        from django.utils import timezone
        current_year = timezone.now().year
        future_year = current_year + 5
        
        data = {
            'title': 'Book from Future',
            'publication_year': future_year,
            'author': self.author1.id
        }
        response = self.client.post('/api/books/create/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Publication year cannot be in the future', str(response.data))
    
    def test_create_book_missing_required_fields(self):
        """Test validation requires all required fields."""
        self.client.force_authenticate(user=self.user)
        
        # Missing title
        data = {
            'publication_year': 2023,
            'author': self.author1.id
        }
        response = self.client.post('/api/books/create/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)
    
    # ==================== PERMISSION TESTS ====================
    
    def test_unauthenticated_user_can_read(self):
        """Test unauthenticated users can read books."""
        # List view
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Detail view
        response = self.client.get(f'/api/books/{self.book1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_unauthenticated_user_cannot_write(self):
        """Test unauthenticated users cannot create, update, or delete."""
        # Create
        data = {'title': 'New Book', 'publication_year': 2023, 'author': self.author1.id}
        response = self.client.post('/api/books/create/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Update
        response = self.client.put(f'/api/books/update/{self.book1.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Delete
        response = self.client.delete(f'/api/books/delete/{self.book1.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_authenticated_user_can_write(self):
        """Test authenticated users can create, update, and delete."""
        self.client.force_authenticate(user=self.user)
        
        # Create
        data = {'title': 'New Book', 'publication_year': 2023, 'author': self.author1.id}
        response = self.client.post('/api/books/create/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Update
        update_data = {'title': 'Updated', 'publication_year': 2023, 'author': self.author1.id}
        response = self.client.put(f'/api/books/update/{self.book1.id}/', update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Delete
        response = self.client.delete(f'/api/books/delete/{self.book1.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
