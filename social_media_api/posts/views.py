from rest_framework import viewsets, filters, generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from .permissions import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend

# Post ViewSet
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title', 'content']
    filterset_fields = ['author']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# Comment ViewSet
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# ===== TASK 2: FEED VIEW =====
class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Get users that the current user follows
        following_users = self.request.user.following.all()
        # Return posts from followed users, ordered by newest first
        return Post.objects.filter(author__in=following_users).order_by('-created_at')

# ===== TASK 3: LIKE FUNCTIONALITY =====
class LikePostView(APIView):
    """View to like a post"""
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response(
                {'error': 'Post not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )

        # Check if user already liked the post
        if Like.objects.filter(user=request.user, post=post).exists():
            return Response(
                {'error': 'You have already liked this post'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create the like
        like = Like.objects.create(user=request.user, post=post)
        serializer = LikeSerializer(like)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UnlikePostView(APIView):
    """View to unlike a post"""
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response(
                {'error': 'Post not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            like = Like.objects.get(user=request.user, post=post)
            like.delete()
            return Response(
                {'message': 'Post unliked successfully'}, 
                status=status.HTTP_204_NO_CONTENT
            )
        except Like.DoesNotExist:
            return Response(
                {'error': 'You have not liked this post'}, 
                status=status.HTTP_400_BAD_REQUEST
            )