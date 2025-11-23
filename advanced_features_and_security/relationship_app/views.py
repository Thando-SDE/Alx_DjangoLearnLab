from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required, login_required
from .models import Book

@login_required
@permission_required('relationship_app.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return HttpResponse(f"Book list view - {books.count()} books")

@login_required  
@permission_required('relationship_app.can_create', raise_exception=True)
def book_create(request):
    return HttpResponse("Book create view - permission granted")

@login_required
@permission_required('relationship_app.can_edit', raise_exception=True)
def book_edit(request, book_id):
    return HttpResponse(f"Book edit view - editing book {book_id}")

@login_required
@permission_required('relationship_app.can_delete', raise_exception=True)
def book_delete(request, book_id):
    return HttpResponse(f"Book delete view - deleting book {book_id}")