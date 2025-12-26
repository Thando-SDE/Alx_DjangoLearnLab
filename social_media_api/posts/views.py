from rest_framework import viewsets, filters, generics
from rest_framework.permissions import IsAuthenticated
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly  # Import from permissions.py
from django_filters.rest_framework import DjangoFilterBackend  # For filtering

# Post ViewSet
class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing, creating, updating, and deleting Posts.
    """
    queryset = Post.objects.all().order_by('-created_at')  # Newest first
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title', 'content']  # For Step 5: Filtering by title or content
    filterset_fields = ['author']  # Optional: filter by author ID

    def perform_create(self, serializer):
        # Automatically set the author to the current user when creating a post
        serializer.save(author=self.request.user)

# Comment ViewSet
class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing, creating, updating, and deleting Comments.
    """
    queryset = Comment.objects.all().order_by('-created_at')  # Newest first
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        # Automatically set the author to the current user when creating a comment
        serializer.save(author=self.request.user)

# ===== TASK 2: FEED VIEW =====

class FeedView(generics.ListAPIView):
    """
    View to get posts from users that the current user follows.
    Ordered by creation date (newest first).
    """
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Get IDs of users that the current user follows
        following_ids = self.request.user.following.values_list('id', flat=True)
        
        # Return posts from followed users, ordered by newest first
        return Post.objects.filter(author__id__in=following_ids).order_by('-created_at')