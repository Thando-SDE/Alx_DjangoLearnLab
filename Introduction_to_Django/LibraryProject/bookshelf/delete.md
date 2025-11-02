# DELETE Operation

## Command:
```python
from bookshelf.models import Book
print(f"Books before deletion: {Book.objects.count()}")
updated_book.delete()
print(f"Books after deletion: {Book.objects.count()}")
try:
    Book.objects.get(id=1)
    print("Book still exists")
except Book.DoesNotExist:
    print("Book successfully deleted - DoesNotExist error raised")
```

## Expected Output:
Book should be deleted and count should go from 1 to 0.

## Actual Output:
Books before deletion: 1
Books after deletion: 0
Book successfully deleted - DoesNotExist error raised
