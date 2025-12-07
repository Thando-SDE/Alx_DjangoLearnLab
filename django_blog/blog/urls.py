from django.urls import path
from . import views
from .views import (
    PostListView, PostDetailView, PostCreateView,
    PostUpdateView, PostDeleteView, CommentCreateView
)

urlpatterns = [
    path('', views.home, name='home'),
    path('posts/', PostListView.as_view(), name='post-list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/comment/', CommentCreateView.as_view(), name='comment-create'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('search/', views.search, name='search'),
    path('tags/<str:tag_name>/', views.posts_by_tag, name='posts-by-tag'),
]
