# CREATE Operation

## Command:
```python
from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
```

## Expected Output:
Book object created successfully with ID.

## Actual Output:
Created book: 1984 by George Orwell (1949)
Book ID: 1
