"""
Step 2 & Step 3: Secure views implementation.
- Step 2: CSRF protection with @csrf_protect decorator
- Step 3: SQL injection prevention using Django ORM
- Secure input validation and sanitization
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.db.models import Q
from django.utils.html import escape
from .models import Book
from .forms import BookForm, ExampleForm


# Step 3: Secure book list view with SQL injection prevention
@csrf_protect
def book_list(request):
    """
    Display books with secure search functionality.
    
    Security measures:
    - Uses Django ORM (prevents SQL injection)
    - Validates search input length
    - Escapes output to prevent XSS
    """
    # Get all books using Django ORM (SAFE - parameterized queries)
    books = Book.objects.all()
    
    # Step 3: Secure search implementation
    search_query = request.GET.get('search', '').strip()
    
    if search_query:
        # Validate search query length
        if len(search_query) > 100:
            messages.error(request, 'Search query is too long.')
            search_query = search_query[:100]
        
        # SECURE: Using Django ORM's Q objects
        # This automatically parameterizes the query, preventing SQL injection
        # NEVER use raw SQL with string formatting like:
        # f"SELECT * FROM books WHERE title LIKE '%{search_query}%'"  <- VULNERABLE!
        books = books.filter(
            Q(title__icontains=search_query) | 
            Q(author__icontains=search_query)
        )
        
        # Escape search query for safe display (prevents XSS)
        safe_search_query = escape(search_query)
    else:
        safe_search_query = ''
    
    return render(request, 'bookshelf/book_list.html', {
        'books': books,
        'search_query': safe_search_query,
    })


# Step 2 & 3: Secure book creation with CSRF protection and validation
@csrf_protect  # Step 2: Explicitly ensure CSRF protection
@require_http_methods(["GET", "POST"])  # Only allow GET and POST methods
@login_required  # Require authentication
@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    """
    Create a book with security measures.
    
    Security features:
    - CSRF token required (Step 2)
    - Form validation (Step 3)
    - Permission checks
    - HTTP method restriction
    """
    if request.method == 'POST':
        # Step 3: Use Django forms for automatic validation and sanitization
        form = BookForm(request.POST)
        
        if form.is_valid():
            # form.cleaned_data contains validated and sanitized data
            book = form.save()
            messages.success(request, 'Book created successfully!')
            return redirect('book_list')
        else:
            # Display form errors
            messages.error(request, 'Please correct the errors below.')
    else:
        # GET request - show empty form
        form = BookForm()
    
    return render(request, 'bookshelf/book_form.html', {
        'form': form,
        'action': 'Create'
    })


# Step 2 & 3: Secure book update view
@csrf_protect
@require_http_methods(["GET", "POST"])
@login_required
@permission_required('bookshelf.can_edit', raise_exception=True)
def book_update(request, pk):
    """
    Update a book securely.
    
    Security measures:
    - get_object_or_404 uses parameterized queries (SQL injection safe)
    - CSRF protection
    - Form validation
    """
    # Step 3: SECURE - get_object_or_404 uses Django ORM
    # This is SAFE from SQL injection
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Book updated successfully!')
            return redirect('book_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BookForm(instance=book)
    
    return render(request, 'bookshelf/book_form.html', {
        'form': form,
        'book': book,
        'action': 'Update'
    })


# Step 2: Secure delete view - POST only to prevent CSRF
@csrf_protect
@require_http_methods(["POST"])  # DELETE must be POST to use CSRF protection
@login_required
@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
    """
    Delete a book securely.
    
    Security measures:
    - POST-only method (prevents CSRF via GET requests)
    - CSRF token required
    - Parameterized query
    """
    # Step 3: SECURE - uses Django ORM
    book = get_object_or_404(Book, pk=pk)
    
    # Escape book title for safe display in message
    book_title = escape(book.title)
    
    book.delete()
    messages.success(request, f'Book "{book_title}" deleted successfully!')
    
    return redirect('book_list')


# Step 2: Example form demonstrating CSRF protection
@csrf_protect
def form_example(request):
    """
    Example view demonstrating CSRF protection.
    
    This view shows how CSRF tokens protect forms.
    Template must include {% csrf_token %} tag.
    """
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        
        if form.is_valid():
            # All data in cleaned_data is validated and sanitized
            clean_data = form.cleaned_data
            messages.success(
                request, 
                f'Form submitted successfully! Name: {escape(clean_data["name"])}'
            )
            return redirect('form_example')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ExampleForm()
    
    return render(request, 'bookshelf/form_example.html', {'form': form})


# Example of what NOT to do (vulnerable code for educational purposes)
"""
VULNERABLE EXAMPLE - NEVER DO THIS:

def vulnerable_search(request):
    # DANGEROUS: String formatting with user input = SQL INJECTION!
    search = request.GET.get('search', '')
    
    # This is VULNERABLE to SQL injection:
    query = f"SELECT * FROM books WHERE title LIKE '%{search}%'"
    
    # An attacker could input: '; DROP TABLE books; --
    # Resulting in: SELECT * FROM books WHERE title LIKE '%'; DROP TABLE books; --%'
    # This would DELETE YOUR ENTIRE TABLE!
    
    # NEVER use:
    # - String formatting: f"...{user_input}..."
    # - String concatenation: "..." + user_input + "..."
    # - % formatting: "...%s..." % user_input
    
    # ALWAYS use Django ORM or parameterized queries!
"""