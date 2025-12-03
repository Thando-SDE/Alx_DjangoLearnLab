from rest_framework import serializers
from django.utils import timezone
from .models import Author, Book


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    
    Serializes all fields of the Book model and includes custom validation
    for the publication_year field to ensure it's not in the future.
    
    Fields:
    - id: Auto-generated primary key
    - title: Book title
    - publication_year: Year of publication
    - author: ForeignKey to Author (displays author ID)
    
    Validation:
    - Custom validate_publication_year method ensures year is not in future
    """
    
    class Meta:
        model = Book
        fields = '__all__'  # Include all model fields
        read_only_fields = ('id',)  # ID is auto-generated, should be read-only
    
    def validate_publication_year(self, value):
        """
        Validate that publication_year is not in the future.
        
        Args:
            value: The publication_year value to validate
            
        Returns:
            The validated value if valid
            
        Raises:
            serializers.ValidationError: If publication_year is in the future
        """
        current_year = timezone.now().year
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. Current year is {current_year}."
            )
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model with nested BookSerializer.
    
    Includes the author's name and a nested representation of all books
    written by the author. The books field is read-only and dynamically
    serializes the related Book objects.
    
    Fields:
    - id: Auto-generated primary key
    - name: Author's name
    - books: Nested BookSerializer for all books by this author (read-only)
    
    Relationship Handling:
    - Uses BookSerializer to serialize the related books
    - The 'books' field corresponds to the related_name in Book.author field
    """
    
    books = BookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'books']  # Include id, name, and nested books
        read_only_fields = ('id',)  # ID is auto-generated, should be read-only
