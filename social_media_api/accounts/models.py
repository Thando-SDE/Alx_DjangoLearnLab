from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    
    # Users who follow this user
    followers = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='user_followers',  # Changed from 'following'
        blank=True
    )
    
    # Users this user follows
    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='user_following',
        blank=True
    )
    
    # Fixed ManyToMany field clashes
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        blank=True
    )
    
    def __str__(self):
        return self.username
