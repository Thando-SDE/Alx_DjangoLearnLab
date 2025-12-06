# Blog Post Management Features Documentation

## Overview
This Django blog project now includes comprehensive CRUD (Create, Read, Update, Delete) operations for blog posts. Authenticated users can create, edit, and delete their own posts, while all users can view posts.

## Features

### 1. CRUD Operations
- **Create**: Authenticated users can create new blog posts
- **Read**: All users can view blog posts (list and detail views)
- **Update**: Post authors can edit their own posts
- **Delete**: Post authors can delete their own posts

### 2. URL Structure
- `/posts/` - List all blog posts
- `/posts/new/` - Create new post (authenticated users only)
- `/posts/<id>/` - View specific post
- `/posts/<id>/edit/` - Edit post (author only)
- `/posts/<id>/delete/` - Delete post (author only)

### 3. Permissions and Security
- **ListView & DetailView**: Accessible to all users
- **CreateView**: Requires authentication (LoginRequiredMixin)
- **UpdateView & DeleteView**: Requires authentication AND user must be the post author (UserPassesTestMixin)
- **CSRF Protection**: All forms include CSRF tokens
- **Data Validation**: All form inputs are validated

## Models

### Post Model Fields:
- `title`: CharField (max_length=200)
- `content`: TextField
- `date_posted`: DateTimeField (default=timezone.now)
- `date_updated`: DateTimeField (auto_now=True)
- `author`: ForeignKey to User model

### Model Methods:
- `__str__()`: Returns post title
- `get_absolute_url()`: Returns URL to post detail
- `snippet()`: Returns first 100 characters of content

## Views (Class-Based)

### 1. PostListView
- Displays all posts in reverse chronological order
- Pagination: 5 posts per page
- Accessible to all users

### 2. PostDetailView
- Displays full post content
- Shows edit/delete buttons for post author
- Accessible to all users

### 3. PostCreateView
- Creates new posts
- Auto-sets author to current user
- Requires authentication

### 4. PostUpdateView
- Edits existing posts
- Only accessible to post author
- Requires authentication

### 5. PostDeleteView
- Deletes posts
- Only accessible to post author
- Requires authentication
- Shows confirmation before deletion

## Templates

### 1. post_list.html
- Lists all posts with titles, authors, and dates
- Shows post snippets (first 100 characters)
- Includes pagination
- "Create New Post" button for authenticated users

### 2. post_detail.html
- Shows full post content
- Edit/Delete buttons for post author
- Back to list link

### 3. post_form.html
- Used for both create and update operations
- Form with title and content fields
- Submit and cancel buttons

### 4. post_confirm_delete.html
- Confirmation page before deletion
- Yes/No options

## Testing Guidelines

### 1. Create Post Test
1. Login with valid credentials
2. Navigate to `/posts/new/`
3. Fill in title and content
4. Submit form
5. Verify post appears in list and detail views

### 2. Edit Post Test
1. Login as post author
2. Navigate to post detail page
3. Click "Edit" button
4. Modify title or content
5. Submit form
6. Verify changes are saved

### 3. Delete Post Test
1. Login as post author
2. Navigate to post detail page
3. Click "Delete" button
4. Confirm deletion
5. Verify post is removed from list

### 4. Permission Tests
1. Try to edit/delete post as non-author (should be denied)
2. Try to create post without login (should redirect to login)
3. Verify all users can view posts

## File Structure
- `blog/models.py`: Updated Post model
- `blog/forms.py`: Added PostForm
- `blog/views.py`: Added CRUD class-based views
- `blog/urls.py`: Updated URL patterns
- `blog/templates/blog/`: All CRUD templates
- `blog/static/css/styles.css`: Updated styling

## Dependencies
- Django 5.2.7 or higher
- Python 3.8 or higher
