import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_blog.settings')
django.setup()

from django.contrib.auth.models import User
from blog.models import Post

print("Step 1: Setting up Django...")

try:
    # Get the user
    user = User.objects.get(username='ThandoDev')
    print(f"✓ Found user: {user.username}")
except User.DoesNotExist:
    print("✗ User 'ThandoDev' not found")
    exit()

print("\nStep 2: Creating test post...")

# Create the test post
test_post = Post.objects.create(
    title='Complete Test Post with All Features',
    content='''# Welcome to Our Django Blog!

This is a complete test post to demonstrate all features of our blog application.

## Features Tested:

1. Tagging System - This post has multiple tags
2. Search Functionality - Search for keywords in this post
3. Comment System - Leave comments below
4. User Authentication - Only logged-in users can comment
5. Author Permissions - Only the author can edit/delete

## Testing Instructions:
- Try clicking on the tags below
- Use the search bar to find this post
- Login and add a comment
- Test the tag filtering feature''',
    author=user
)

print(f"✓ Created post: '{test_post.title}'")
print(f"✓ Post ID: {test_post.id}")

print("\nStep 3: Adding tags...")
# Add multiple tags
tags_to_add = ['django', 'python', 'testing', 'tutorial', 'web-development', 'blog', 'demo']
test_post.tags.add(*tags_to_add)
test_post.save()

print(f"✓ Added {len(tags_to_add)} tags: {', '.join(tags_to_add)}")

print("\n" + "="*50)
print("COMPLETE!")
print(f"You can view this post at: http://127.0.0.1:8000/post/{test_post.id}/")
print("="*50)
