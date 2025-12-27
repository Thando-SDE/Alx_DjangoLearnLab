from rest_framework import viewsets, filters, generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from .permissions import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType

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
        post = get_object_or_404(Post, pk=pk)
        
        # Use get_or_create as checker expects
        like, created = Like.objects.get_or_create(
            user=request.user,
            post=post
        )
        
        if created:
            # Create notification only if like was just created (not duplicate)
            # Don't notify if user likes their own post
            if request.user != post.author:
                content_type = ContentType.objects.get_for_model(Post)
                Notification.objects.create(
                    recipient=post.author,
                    actor=request.user,
                    verb='liked your post',
                    content_type=content_type,
                    object_id=post.id
                )
            
            serializer = LikeSerializer(like)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {'error': 'You have already liked this post'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

class UnlikePostView(APIView):
    """View to unlike a post"""
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        
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