# RETRIEVE Operation

## Command:
```python
from bookshelf.models import Book
book = Book.objects.get(id=1)
print(f"Title: {book.title}")
print(f"Author: {book.author}")
print(f"Publication Year: {book.publication_year}")
print(f"Full book object: {book}")
```

## Expected Output:
All attributes of the book should be displayed.

## Actual Output:
Title: 1984
Author: George Orwell
Publication Year: 1949
Full book object: 1984
