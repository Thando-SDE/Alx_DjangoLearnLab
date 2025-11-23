"""
Step 3: Secure forms with input validation and sanitization.
Protects against XSS attacks and validates all user input.
"""

from django import forms
from django.core.exceptions import ValidationError
from .models import Book
import bleach


class BookForm(forms.ModelForm):
    """
    Secure form for Book model with comprehensive validation.
    
    Security features:
    - Automatic HTML escaping by Django
    - Custom validators for additional security
    - Input sanitization using bleach library
    """
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year', 'isbn', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter book title',
                'maxlength': 200  # Prevents excessively long input
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter author name',
                'maxlength': 100
            }),
            'publication_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1000,
                'max': 2100
            }),
            'isbn': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter ISBN',
                'maxlength': 13
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter book description',
                'maxlength': 1000
            }),
        }
    
    def clean_title(self):
        """
        Step 3: Validate and sanitize book title.
        Prevents XSS attacks and malicious input.
        """
        title = self.cleaned_data.get('title', '').strip()
        
        # Check if title is empty
        if not title:
            raise ValidationError('Title cannot be empty.')
        
        # Minimum length validation
        if len(title) < 2:
            raise ValidationError('Title must be at least 2 characters long.')
        
        # Maximum length validation
        if len(title) > 200:
            raise ValidationError('Title must not exceed 200 characters.')
        
        # Check for script tags and JavaScript (XSS protection)
        if '<script>' in title.lower() or 'javascript:' in title.lower():
            raise ValidationError('Invalid characters detected in title.')
        
        return title
    
    def clean_author(self):
        """Validate author name."""
        author = self.cleaned_data.get('author', '').strip()
        
        if not author:
            raise ValidationError('Author name cannot be empty.')
        
        if len(author) < 2:
            raise ValidationError('Author name must be at least 2 characters long.')
        
        return author
    
    def clean_publication_year(self):
        """Validate publication year range."""
        year = self.cleaned_data.get('publication_year')
        
        if year:
            if year < 1000 or year > 2100:
                raise ValidationError('Please enter a valid publication year between 1000 and 2100.')
        
        return year
    
    def clean_isbn(self):
        """
        Validate ISBN format.
        Accepts ISBN-10 or ISBN-13 formats.
        """
        isbn = self.cleaned_data.get('isbn', '').strip()
        
        if isbn:
            # Remove hyphens and spaces
            isbn_clean = isbn.replace('-', '').replace(' ', '')
            
            # Check length
            if not (len(isbn_clean) == 10 or len(isbn_clean) == 13):
                raise ValidationError('ISBN must be 10 or 13 digits long.')
            
            # Check if all characters are digits
            if not isbn_clean.isdigit():
                raise ValidationError('ISBN must contain only digits.')
        
        return isbn
    
    def clean_description(self):
        """
        Step 3: Sanitize description field using bleach.
        Allows only safe HTML tags to prevent XSS attacks.
        """
        description = self.cleaned_data.get('description', '').strip()
        
        if description:
            # Define allowed HTML tags (very limited for security)
            allowed_tags = ['p', 'br', 'strong', 'em', 'u']
            allowed_attributes = {}  # No attributes allowed
            
            # Use bleach to sanitize HTML and remove dangerous content
            description = bleach.clean(
                description,
                tags=allowed_tags,
                attributes=allowed_attributes,
                strip=True  # Remove disallowed tags completely
            )
        
        return description


class ExampleForm(forms.Form):
    """
    Example form demonstrating various security validations.
    Used for Step 2: CSRF protection demonstration.
    """
    
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your name'
        }),
        help_text='Maximum 100 characters'
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )
    
    message = forms.CharField(
        max_length=500,
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Enter your message'
        })
    )
    
    def clean_name(self):
        """
        Step 3: Validate and sanitize name field.
        Prevents XSS attacks.
        """
        name = self.cleaned_data.get('name', '').strip()
        
        if not name:
            raise ValidationError('Name cannot be empty.')
        
        # Check for HTML/script injection attempts
        if '<' in name or '>' in name or 'script' in name.lower():
            raise ValidationError('Name contains invalid characters.')
        
        return name
    
    def clean_message(self):
        """Sanitize message field - remove all HTML."""
        message = self.cleaned_data.get('message', '').strip()
        
        if message:
            # Use bleach to remove ALL HTML tags for safety
            message = bleach.clean(message, tags=[], strip=True)
        
        return message