from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'bio', 'profile_picture', 'followers']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'bio', 'profile_picture']
        extra_kwargs = {
            'username': {'validators': []}
        }
    
    def create(self, validated_data):
        # Use create_user method for proper password hashing
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        
        # Add optional fields
        user.bio = validated_data.get('bio', '')
        if 'profile_picture' in validated_data:
            user.profile_picture = validated_data['profile_picture']
        user.save()
        
        # Create token for the user
        Token.objects.create(user=user)
        
        return user