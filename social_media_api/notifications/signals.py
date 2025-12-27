from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from posts.models import Like, Comment
from accounts.models import CustomUser
from .models import Notification

@receiver(post_save, sender=Like)
def create_like_notification(sender, instance, created, **kwargs):
    """Create notification when someone likes a post"""
    if created:
        # Don't notify if user likes their own post
        if instance.user != instance.post.author:
            content_type = ContentType.objects.get_for_model(instance.post)
            
            Notification.objects.create(
                recipient=instance.post.author,
                actor=instance.user,
                verb='liked your post',
                content_type=content_type,
                object_id=instance.post.id
            )

@receiver(post_save, sender=CustomUser.following.through)
def create_follow_notification(sender, instance, created, **kwargs):
    """Create notification when someone follows a user"""
    if created:
        # instance is the follow relationship
        from_user = instance.from_user
        to_user = instance.to_user
        
        content_type = ContentType.objects.get_for_model(to_user)
        
        Notification.objects.create(
            recipient=to_user,
            actor=from_user,
            verb='started following you',
            content_type=content_type,
            object_id=to_user.id
        )

@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    """Create notification when someone comments on a post"""
    if created:
        # Don't notify if user comments on their own post
        if instance.author != instance.post.author:
            content_type = ContentType.objects.get_for_model(instance.post)
            
            Notification.objects.create(
                recipient=instance.post.author,
                actor=instance.author,
                verb='commented on your post',
                content_type=content_type,
                object_id=instance.post.id
            )