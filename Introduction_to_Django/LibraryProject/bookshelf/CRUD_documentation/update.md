# UPDATE Operation

## Command:
```python
from bookshelf.models import Book
book = Book.objects.get(id=1)
print(f"Current title: {book.title}")
book.title = "Nineteen Eighty-Four"
book.save()
updated_book = Book.objects.get(id=1)
print(f"Updated title: {updated_book.title}")
```

## Expected Output:
Title should be updated from '1984' to 'Nineteen Eighty-Four'.

## Actual Output:
Current title: 1984
Updated title: Nineteen Eighty-Four
