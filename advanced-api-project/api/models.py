from django.db import models


class Author(models.Model):
    """
    Author model represents an author of books.
    
    Fields:
    - name: The full name of the author (CharField, max_length=100)
    
    Relationship:
    - One Author can have multiple Books (one-to-many relationship)
    """
    name = models.CharField(max_length=100)
    
    def __str__(self):
        """String representation of Author model."""
        return self.name
    
    class Meta:
        """Metadata options for Author model."""
        ordering = ['name']  # Order authors alphabetically by name


class Book(models.Model):
    """
    Book model represents a book written by an author.
    
    Fields:
    - title: The title of the book (CharField, max_length=200)
    - publication_year: The year the book was published (IntegerField)
    - author: ForeignKey relationship to Author model (many-to-one)
    
    Relationship:
    - Each Book belongs to one Author
    - One Author can have multiple Books
    """
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(
        Author, 
        on_delete=models.CASCADE,  # If author is deleted, delete their books
        related_name='books'  # Access author's books via author.books.all()
    )
    
    def __str__(self):
        """String representation of Book model."""
        return f"{self.title} ({self.publication_year})"
    
    class Meta:
        """Metadata options for Book model."""
        ordering = ['title']  # Order books alphabetically by title
        # Ensure unique constraint: same title by same author in same year
        unique_together = ['title', 'author', 'publication_year']
