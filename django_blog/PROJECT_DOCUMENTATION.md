# Django Blog Project Documentation

## Project Overview
A complete Django blog application with advanced tagging and search functionality built with Django and django-taggit.

## Features Implemented

### 1. Tagging System
- **How to add tags to posts:**
  1. Create or edit a post using the "New Post" or "Update Post" forms
  2. In the "Tags" field, enter tags separated by commas (e.g., "django, python, web-development")
  3. Submit the form - tags are automatically created and associated with the post
  4. Tags display as clickable badges on all post views

- **How to use tags:**
  - Click any tag badge on a post to see all posts with that tag
  - Tags support filtering and organization of content
  - Multiple tags can be assigned to each post

### 2. Search Functionality
- **How to use the search bar:**
  1. The search bar is available in the top navigation on all pages
  2. Enter keywords in the search box and press Enter or click the search icon
  3. Search looks through:
     - Post titles
     - Post content
     - Tag names
  4. Results are displayed on a dedicated search results page

- **Search by tags:**
  - You can also search for specific tags using the tag badges
  - Clicking a tag shows all posts with that tag

### 3. User Authentication
- User registration, login, and profile management
- Only authenticated users can create posts and comments
- Authors can edit/delete their own posts

### 4. Post Management
- Create, read, update, and delete blog posts
- Rich content support with formatting
- Automatic timestamps for post creation and updates

### 5. Comment System
- Authenticated users can comment on posts
- Comments display in chronological order
- Simple form for adding comments

## Technical Implementation

### Models
- `Post`: Includes TaggableManager from django-taggit for tag management
- `Comment`: Related to posts with foreign key relationships
- Uses django-taggit for efficient tag storage and retrieval

### Views
- `search()`: Uses Django Q objects for complex search queries across titles, content, and tags
- `posts_by_tag()`: Filters posts by specific tag names
- Class-based views for CRUD operations
- Function-based views for search and tag filtering

### Templates
- `base.html`: Includes search bar in navigation
- `post_detail.html`: Displays tags as clickable badges
- `search_results.html`: Shows search results with statistics
- `posts_by_tag.html`: Displays posts filtered by tag

### URLs
- `/search/`: Handles search queries
- `/tags/<tag_name>/`: Shows posts with specific tag

## Setup Instructions

```bash
# Install requirements
pip install django django-taggit

# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

## Testing the Features

1. **Test tagging:**
   - Create a post with tags like "django, tutorial"
   - Verify tags appear as clickable badges
   - Click a tag to see filtered posts

2. **Test search:**
   - Use the search bar to search for "django"
   - Verify results include posts with "django" in title, content, or tags
   - Test searching for specific tags

3. **Test user features:**
   - Register a new user
   - Create posts with tags
   - Add comments to posts
