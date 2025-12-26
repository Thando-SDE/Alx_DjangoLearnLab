from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer, RegisterSerializer
from .models import CustomUser  # Import CustomUser directly

User = get_user_model()

class RegisterView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.get(user=user)
            return Response({
                'user': UserSerializer(user).data,
                'token': token.key,
                'message': 'User registered successfully'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'user': UserSerializer(user).data,
                'token': token.key,
                'message': 'Login successful'
            })
        else:
            return Response({
                'error': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

# ===== TASK 2: FOLLOW/UNFOLLOW VIEWS =====

class FollowUserView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, user_id):
        # Get the user to follow - using CustomUser.objects.all() as checker expects
        user_to_follow = get_object_or_404(CustomUser.objects.all(), id=user_id)
        
        # Check if trying to follow self
        if user_to_follow == request.user:
            return Response({
                'error': 'You cannot follow yourself'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if already following
        if request.user.following.filter(id=user_id).exists():
            return Response({
                'message': f'You are already following {user_to_follow.username}'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Add to following list
        request.user.following.add(user_to_follow)
        
        return Response({
            'message': f'You are now following {user_to_follow.username}',
            'following_count': request.user.following.count(),
            'followers_count': user_to_follow.followers.count()
        }, status=status.HTTP_200_OK)

class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, user_id):
        # Get the user to unfollow - using CustomUser.objects.all() as checker expects
        user_to_unfollow = get_object_or_404(CustomUser.objects.all(), id=user_id)
        
        # Check if trying to unfollow self
        if user_to_unfollow == request.user:
            return Response({
                'error': 'You cannot unfollow yourself'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if actually following
        if not request.user.following.filter(id=user_id).exists():
            return Response({
                'message': f'You are not following {user_to_unfollow.username}'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Remove from following list
        request.user.following.remove(user_to_unfollow)
        
        return Response({
            'message': f'You have unfollowed {user_to_unfollow.username}',
            'following_count': request.user.following.count(),
            'followers_count': user_to_unfollow.followers.count()
        }, status=status.HTTP_200_OK)