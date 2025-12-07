# Comment Functionality Documentation

## Overview
This Django blog project now includes a comprehensive comment system that allows users to interact with blog posts. Authenticated users can post, edit, and delete their comments, while all users can read comments.

## Features

### 1. Comment Model
- **post**: ForeignKey to Post model (many-to-one relationship)
- **author**: ForeignKey to User model
- **content**: TextField for comment text
- **created_at**: DateTimeField (auto_now_add)
- **updated_at**: DateTimeField (auto_now)
- **ordering**: Comments displayed newest first

### 2. CRUD Operations for Comments
- **Create**: Authenticated users can post comments on any blog post
- **Read**: All users can view comments
- **Update**: Comment authors can edit their own comments
- **Delete**: Comment authors can delete their own comments

### 3. URL Structure
- `/post/<id>/` - View post with comments (includes comment form)
- `/comment/<id>/update/` - Edit comment (author only)
- `/comment/<id>/delete/` - Delete comment (author only)

### 4. Permissions and Security
- **View Comments**: Accessible to all users
- **Create Comments**: Requires authentication
- **Update/Delete Comments**: Requires authentication AND user must be comment author
- **CSRF Protection**: All forms include CSRF tokens
- **Data Validation**: All form inputs are validated

## Models

### Comment Model Fields:
- `post`: ForeignKey to Post (CASCADE delete)
- `author`: ForeignKey to User (CASCADE delete)
- `content`: TextField
- `created_at`: DateTimeField (auto_now_add=True)
- `updated_at`: DateTimeField (auto_now=True)

### Model Methods:
- `__str__()`: Returns "Comment by [author] on [post title]"
- Meta ordering: `['-created_at']` (newest first)

## Views

### 1. Post Detail View (updated)
- Displays post with all comments
- Includes comment form for authenticated users
- Shows edit/delete buttons for comment authors

### 2. CommentUpdateView (Class-Based)
- Edits existing comments
- Only accessible to comment author
- Uses `LoginRequiredMixin` and `UserPassesTestMixin`
- Redirects back to post detail page after update

### 3. CommentDeleteView (Class-Based)
- Deletes comments
- Only accessible to comment author
- Uses `LoginRequiredMixin` and `UserPassesTestMixin`
- Shows confirmation before deletion
- Redirects back to post detail page after delete

## Templates

### 1. post_detail.html (updated)
- Shows post content
- Displays all comments with authors and timestamps
- Includes comment form for authenticated users
- Shows edit/delete buttons for comment authors
- Login prompt for unauthenticated users

### 2. comment_form.html
- Form for editing comments
- Shows which post the comment belongs to
- Submit and cancel buttons

### 3. comment_confirm_delete.html
- Confirmation page before deleting comment
- Shows comment preview
- Yes/No options

## Testing Guidelines

### 1. Create Comment Test
1. Login with valid credentials
2. Navigate to any post detail page
3. Fill in comment form
4. Submit form
5. Verify comment appears in comments section

### 2. Edit Comment Test
1. Login as comment author
2. Navigate to post with your comment
3. Click "Edit" button on your comment
4. Modify comment content
5. Submit form
6. Verify changes are saved

### 3. Delete Comment Test
1. Login as comment author
2. Navigate to post with your comment
3. Click "Delete" button on your comment
4. Confirm deletion
5. Verify comment is removed

### 4. Permission Tests
1. Try to edit/delete comment as non-author (should be denied)
2. Try to post comment without login (should see login prompt)
3. Verify all users can view comments

## File Structure
- `blog/models.py`: Added Comment model
- `blog/forms.py`: Added CommentForm
- `blog/views.py`: Updated post_detail view, added CommentUpdateView and CommentDeleteView
- `blog/urls.py`: Added comment URLs
- `blog/templates/blog/`: Added comment_form.html and comment_confirm_delete.html
- `blog/static/css/styles.css`: Added comment styling

## Dependencies
- Django 5.2.7 or higher
- Python 3.8 or higher
