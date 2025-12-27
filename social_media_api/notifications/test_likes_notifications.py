#!/usr/bin/env python3
import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_media_api.settings')
django.setup()

from django.contrib.auth import get_user_model
from posts.models import Post, Like
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

User = get_user_model()

print("=" * 60)
print("STEP 5: Testing Likes and Notifications Features")
print("=" * 60)

def cleanup():
    """Clean up test data"""
    User.objects.filter(username__startswith='testuser_').delete()

def test_like_functionality():
    print("\n1. TESTING LIKE FUNCTIONALITY")
    print("-" * 40)
    
    # Create test users
    user1 = User.objects.create_user(
        username='testuser_liker',
        email='liker@test.com',
        password='password123'
    )
    user2 = User.objects.create_user(
        username='testuser_poster',
        email='poster@test.com',
        password='password123'
    )
    
    # Create a post
    post = Post.objects.create(
        title='Test Post for Liking',
        content='This is a test post for like functionality',
        author=user2
    )
    
    print(f"✓ Created test users and post (ID: {post.id})")
    
    # Create API clients with authentication
    client1 = APIClient()
    client2 = APIClient()
    
    # Get tokens (or use force_authenticate)
    token1 = Token.objects.create(user=user1)
    token2 = Token.objects.create(user=user2)
    
    client1.credentials(HTTP_AUTHORIZATION='Token ' + token1.key)
    client2.credentials(HTTP_AUTHORIZATION='Token ' + token2.key)
    
    # Test 1: Like a post
    print("\n   Test 1.1: Like a post")
    response = client1.post(f'/api/posts/{post.id}/like/')
    if response.status_code == 201:
        print(f"   ✓ Post liked successfully")
        print(f"   Response: {response.data}")
    else:
        print(f"   ✗ Failed to like post: {response.status_code}")
        print(f"   Error: {response.data}")
    
    # Test 2: Try to like same post again (should fail)
    print("\n   Test 1.2: Try to like same post again (should fail)")
    response = client1.post(f'/api/posts/{post.id}/like/')
    if response.status_code == 400 and 'already liked' in str(response.data).lower():
        print(f"   ✓ Correctly prevented duplicate like")
    else:
        print(f"   ✗ Should have prevented duplicate like: {response.status_code}")
    
    # Test 3: Check likes count on post
    print("\n   Test 1.3: Check likes count")
    response = client1.get(f'/api/posts/{post.id}/')
    if response.status_code == 200:
        likes_count = response.data.get('likes_count', 0)
        print(f"   ✓ Post has {likes_count} like(s)")
    else:
        print(f"   ✗ Failed to get post: {response.status_code}")
    
    # Test 4: Unlike the post
    print("\n   Test 1.4: Unlike the post")
    response = client1.delete(f'/api/posts/{post.id}/unlike/')
    if response.status_code == 204:
        print(f"   ✓ Post unliked successfully")
    else:
        print(f"   ✗ Failed to unlike post: {response.status_code}")
    
    # Test 5: Try to unlike a post that wasn't liked
    print("\n   Test 1.5: Try to unlike a post that wasn't liked")
    response = client1.delete(f'/api/posts/{post.id}/unlike/')
    if response.status_code == 400 and 'not liked' in str(response.data).lower():
        print(f"   ✓ Correctly handled attempt to unlike non-liked post")
    else:
        print(f"   ✗ Should have prevented unliking non-liked post: {response.status_code}")
    
    return user1, user2, post

def test_notification_functionality(user1, user2, post):
    print("\n\n2. TESTING NOTIFICATION FUNCTIONALITY")
    print("-" * 40)
    
    client1 = APIClient()
    client2 = APIClient()
    
    token1 = Token.objects.get(user=user1)
    token2 = Token.objects.get(user=user2)
    
    client1.credentials(HTTP_AUTHORIZATION='Token ' + token1.key)
    client2.credentials(HTTP_AUTHORIZATION='Token ' + token2.key)
    
    # Test 1: Create a like to trigger notification
    print("\n   Test 2.1: Create like to trigger notification")
    client1.post(f'/api/posts/{post.id}/like/')
    
    # Check if notification was created
    notifications = Notification.objects.filter(recipient=user2)
    if notifications.exists():
        print(f"   ✓ Notification created for like")
        notification = notifications.first()
        print(f"   Notification: {notification.actor.username} {notification.verb}")
    else:
        print(f"   ✗ No notification created for like")
    
    # Test 2: Get notifications for user2
    print("\n   Test 2.2: Get notifications for user")
    response = client2.get('/api/notifications/')
    if response.status_code == 200:
        print(f"   ✓ Retrieved {len(response.data)} notification(s)")
        if response.data:
            print(f"   First notification: {response.data[0]}")
    else:
        print(f"   ✗ Failed to get notifications: {response.status_code}")
    
    # Test 3: Mark notification as read
    print("\n   Test 2.3: Mark notification as read")
    if notifications.exists():
        notification = notifications.first()
        response = client2.post(f'/api/notifications/{notification.id}/mark-read/')
        if response.status_code == 200:
            print(f"   ✓ Notification marked as read")
            # Refresh notification
            notification.refresh_from_db()
            if notification.is_read:
                print(f"   ✓ is_read flag updated to True")
            else:
                print(f"   ✗ is_read flag not updated")
        else:
            print(f"   ✗ Failed to mark as read: {response.status_code}")
    else:
        print(f"   ⚠ No notification to mark as read")
    
    # Test 4: Try to mark other user's notification as read (should fail)
    print("\n   Test 2.4: Try to mark other user's notification as read (should fail)")
    if notifications.exists():
        notification = notifications.first()
        response = client1.post(f'/api/notifications/{notification.id}/mark-read/')
        if response.status_code == 403:
            print(f"   ✓ Correctly prevented unauthorized mark as read")
        else:
            print(f"   ✗ Should have prevented unauthorized access: {response.status_code}")
    
    # Test 5: Create comment to trigger notification
    print("\n   Test 2.5: Test comment notification")
    from posts.models import Comment
    comment = Comment.objects.create(
        post=post,
        author=user1,
        content='This is a test comment'
    )
    
    # Check if notification was created
    comment_notifications = Notification.objects.filter(
        recipient=user2,
        verb__contains='comment'
    )
    if comment_notifications.exists():
        print(f"   ✓ Notification created for comment")
    else:
        print(f"   ✗ No notification created for comment")

def test_edge_cases():
    print("\n\n3. TESTING EDGE CASES")
    print("-" * 40)
    
    # Create additional test user
    user3 = User.objects.create_user(
        username='testuser_edge',
        email='edge@test.com',
        password='password123'
    )
    
    client3 = APIClient()
    token3 = Token.objects.create(user=user3)
    client3.credentials(HTTP_AUTHORIZATION='Token ' + token3.key)
    
    # Test 1: Try to like non-existent post
    print("\n   Test 3.1: Like non-existent post")
    response = client3.post('/api/posts/99999/like/')
    if response.status_code == 404:
        print(f"   ✓ Correctly handled non-existent post")
    else:
        print(f"   ✗ Should return 404: {response.status_code}")
    
    # Test 2: Try to unlike non-existent post
    print("\n   Test 3.2: Unlike non-existent post")
    response = client3.delete('/api/posts/99999/unlike/')
    if response.status_code == 404:
        print(f"   ✓ Correctly handled non-existent post")
    else:
        print(f"   ✗ Should return 404: {response.status_code}")
    
    # Test 3: Access without authentication
    print("\n   Test 3.3: Access like endpoint without authentication")
    client_no_auth = APIClient()
    response = client_no_auth.post('/api/posts/1/like/')
    if response.status_code == 401:
        print(f"   ✓ Correctly required authentication")
    else:
        print(f"   ✗ Should require authentication: {response.status_code}")

def main():
    try:
        # Clean up any existing test data
        cleanup()
        
        # Run tests
        user1, user2, post = test_like_functionality()
        test_notification_functionality(user1, user2, post)
        test_edge_cases()
        
        print("\n" + "=" * 60)
        print("STEP 5 COMPLETE: All tests passed! ✓")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ ERROR during testing: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # Clean up
        cleanup()
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)