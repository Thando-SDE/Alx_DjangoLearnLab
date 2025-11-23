"""
URL configuration for bookshelf app with secure routing.
"""

from django.urls import path
from . import views

app_name = 'bookshelf'

urlpatterns = [
    # Public view - book list with search
    path('', views.book_list, name='book_list'),
    
    # Step 2 & 3: Protected views with CSRF and validation
    path('create/', views.book_create, name='book_create'),
    path('<int:pk>/edit/', views.book_update, name='book_update'),
    path('<int:pk>/delete/', views.book_delete, name='book_delete'),
    
    # Step 2: CSRF protection example
    path('csrf-example/', views.form_example, name='form_example'),
]