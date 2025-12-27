# Social Media API Documentation
## Complete API Reference (Tasks 0-3)

### Authentication
All endpoints require token authentication except where noted.
Include token in request header:
Authorization: Token <your_token>

### Base URL
`http://127.0.0.1:8000/api/`

---

## AUTHENTICATION ENDPOINTS (Task 0)

### 1. Register User
**POST** `/api/accounts/register/`

**Request Body:**
```json
{
  "username": "newuser",
  "email": "user@example.com",
  "password": "password123",
  "bio": "Optional user bio",
  "profile_picture": "Optional URL or path"
}
Response (201 Created):

json
{
  "id": 1,
  "username": "newuser",
  "email": "user@example.com",
  "bio": "Optional user bio",
  "profile_picture": null,
  "token": "your_auth_token_here"
}
2. Login
POST /api/accounts/login/

Request Body:

json
{
  "username": "newuser",
  "password": "password123"
}
Response (200 OK):

json
{
  "token": "your_auth_token_here",
  "user": {
    "id": 1,
    "username": "newuser",
    "email": "user@example.com",
    "bio": "User bio here",
    "profile_picture": null
  }
}
3. Get User Profile
GET /api/accounts/profile/

Response (200 OK):

json
{
  "id": 1,
  "username": "newuser",
  "email": "user@example.com",
  "bio": "User bio here",
  "profile_picture": null,
  "followers_count": 5,
  "following_count": 3
}
POSTS ENDPOINTS (Task 1)
1. List All Posts
GET /posts/

Query Parameters:

page (optional): Page number for pagination (default: 1)

page_size (optional): Items per page (default: 10, max: 100)

search (optional): Search in title or content

author (optional): Filter by author ID

Response (200 OK):

json
{
  "count": 2,
  "next": "http://127.0.0.1:8000/api/posts/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "My First Post",
      "content": "Post content",
      "author": {
        "id": 1,
        "username": "newuser",
        "email": "newuser@example.com",
        "bio": "User bio",
        "profile_picture": null
      },
      "author_id": 1,
      "created_at": "2025-12-27T10:30:00Z",
      "updated_at": "2025-12-27T10:30:00Z",
      "comments_count": 3,
      "likes_count": 5
    }
  ]
}
2. Create a Post
POST /posts/

Request Body:

json
{
  "title": "Post Title",
  "content": "Post content here"
}
Response (201 Created):

json
{
  "id": 2,
  "title": "Post Title",
  "content": "Post content here",
  "author": {
    "id": 1,
    "username": "newuser",
    "email": "newuser@example.com",
    "bio": "User bio",
    "profile_picture": null
  },
  "author_id": 1,
  "created_at": "2025-12-27T10:35:00Z",
  "updated_at": "2025-12-27T10:35:00Z",
  "comments_count": 0,
  "likes_count": 0
}
3. Retrieve a Single Post
GET /posts/{id}/

Response (200 OK): Complete post object with author details

4. Update a Post
PUT/PATCH /posts/{id}/

Permissions: Only the post author can update.

Request Body (PATCH example):

json
{
  "title": "Updated Title"
}
Response (200 OK): Updated post object.

5. Delete a Post
DELETE /posts/{id}/

Permissions: Only the post author can delete.

Response (204 No Content): Empty response.

COMMENTS ENDPOINTS (Task 1)
1. List All Comments
GET /comments/

Query Parameters:

page (optional): Page number for pagination

page_size (optional): Items per page

Response (200 OK): Paginated list of comments.

2. Create a Comment
POST /comments/

Request Body:

json
{
  "post": 1,
  "content": "This is a comment"
}
Response (201 Created):

json
{
  "id": 1,
  "post": 1,
  "post_title": "My First Post",
  "author": {
    "id": 2,
    "username": "commenter",
    "email": "commenter@example.com",
    "bio": "User bio",
    "profile_picture": null
  },
  "author_id": 2,
  "content": "This is a comment",
  "created_at": "2025-12-27T10:40:00Z",
  "updated_at": "2025-12-27T10:40:00Z"
}
3. Retrieve a Single Comment
GET /comments/{id}/

Response (200 OK): Comment object.

4. Update a Comment
PUT/PATCH /comments/{id}/

Permissions: Only the comment author can update.

5. Delete a Comment
DELETE /comments/{id}/

Permissions: Only the comment author can delete.

FOLLOW/UNFOLLOW ENDPOINTS (Task 2)
1. Follow a User
POST /api/accounts/follow/{user_id}/

Permissions: Authenticated users only.

Request: No body required.

Response (200 OK):

json
{
  "message": "You are now following username",
  "following_count": 1,
  "followers_count": 0
}
Error Responses:

400 Bad Request: Trying to follow yourself

400 Bad Request: Already following this user

404 Not Found: User not found

2. Unfollow a User
POST /api/accounts/unfollow/{user_id}/

Permissions: Authenticated users only.

Request: No body required.

Response (200 OK):

json
{
  "message": "You have unfollowed username",
  "following_count": 0,
  "followers_count": 0
}
Error Responses:

400 Bad Request: Trying to unfollow yourself

400 Bad Request: Not following this user

404 Not Found: User not found

FEED ENDPOINT (Task 2)
Get Followed Users' Posts Feed
GET /api/feed/

Permissions: Authenticated users only.

Description: Returns posts from users that the current user follows, ordered by creation date (newest first).

Response (200 OK):

json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 2,
      "title": "Post from followed user",
      "content": "This should appear in feed!",
      "author": {
        "id": 2,
        "username": "followed_user",
        "email": "followed@example.com",
        "bio": "User bio",
        "profile_picture": null
      },
      "author_id": 2,
      "created_at": "2025-12-27T10:45:00Z",
      "updated_at": "2025-12-27T10:45:00Z",
      "comments_count": 0,
      "likes_count": 0
    }
  ]
}
LIKES ENDPOINTS (Task 3)
1. Like a Post
POST /posts/{post_id}/like/

Permissions: Authenticated users only.

Request: No body required.

Response (201 Created):

json
{
  "id": 1,
  "user": 2,
  "post": 5,
  "created_at": "2025-12-27T10:50:00Z"
}
Error Responses:

400 Bad Request: User has already liked this post

404 Not Found: Post does not exist

401 Unauthorized: Authentication required

2. Unlike a Post
DELETE /posts/{post_id}/unlike/

Permissions: Authenticated users only.

Request: No body required.

Response (204 No Content):

json
{
  "message": "Post unliked successfully"
}
Error Responses:

400 Bad Request: User has not liked this post

404 Not Found: Post does not exist

401 Unauthorized: Authentication required

NOTIFICATIONS ENDPOINTS (Task 3)
1. List Notifications
GET /notifications/

Permissions: Authenticated users only.

Description: Returns all notifications for the current user, ordered by timestamp (newest first).

Response (200 OK):

json
[
  {
    "id": 1,
    "recipient": 2,
    "actor": {
      "id": 3,
      "username": "johndoe",
      "email": "john@example.com",
      "bio": "John's bio",
      "profile_picture": null
    },
    "actor_username": "johndoe",
    "verb": "liked your post",
    "target": 5,
    "is_read": false,
    "timestamp": "2025-12-27T10:30:00Z"
  },
  {
    "id": 2,
    "recipient": 2,
    "actor": {
      "id": 4,
      "username": "janedoe",
      "email": "jane@example.com",
      "bio": "Jane's bio",
      "profile_picture": null
    },
    "actor_username": "janedoe",
    "verb": "started following you",
    "target": 2,
    "is_read": true,
    "timestamp": "2025-12-27T09:15:00Z"
  }
]
2. Mark Notification as Read
POST /notifications/{notification_id}/mark-read/

Permissions: Authenticated users only (can only mark own notifications as read).

Request: No body required.

Response (200 OK):

json
{
  "id": 1,
  "recipient": 2,
  "actor": {
    "id": 3,
    "username": "johndoe",
    "email": "john@example.com",
    "bio": "John's bio",
    "profile_picture": null
  },
  "actor_username": "johndoe",
  "verb": "liked your post",
  "target": 5,
  "is_read": true,
  "timestamp": "2025-12-27T10:30:00Z"
}
Error Responses:

403 Forbidden: Cannot mark another user's notification as read

404 Not Found: Notification does not exist

401 Unauthorized: Authentication required

AUTOMATIC NOTIFICATIONS (Task 3)
The system automatically creates notifications for these actions:

1. Likes
When: User A likes User B's post
Notification: "User A liked your post"
Condition: Not created for self-likes

2. Comments
When: User A comments on User B's post
Notification: "User A commented on your post"
Condition: Not created for self-comments

3. Follows
When: User A follows User B
Notification: "User A started following you"
Condition: Not created for self-follows

PAGINATION
All list endpoints support pagination with default page size of 10:

page: Page number (default: 1)

page_size: Items per page (default: 10, max: 100)

Response Format:

json
{
  "count": 25,
  "next": "http://127.0.0.1:8000/api/posts/?page=2",
  "previous": null,
  "results": [...]
}
PERMISSIONS SUMMARY
Public (No authentication required):

Register (POST /api/accounts/register/)

Login (POST /api/accounts/login/)

Authenticated Users Only:

All POST, PUT, PATCH, DELETE operations

User profile (GET /api/accounts/profile/)

Follow/Unfollow endpoints

Feed endpoint

Likes/Unlikes endpoints

Notifications endpoints

Owner-Only Operations:

Update/Delete own posts

Update/Delete own comments

Mark own notifications as read

TESTING EXAMPLES
Using curl:
bash
# Like a post
curl -X POST http://127.0.0.1:8000/api/posts/5/like/ \
  -H "Authorization: Token your_token_here"

# Unlike a post
curl -X DELETE http://127.0.0.1:8000/api/posts/5/unlike/ \
  -H "Authorization: Token your_token_here"

# Get notifications
curl http://127.0.0.1:8000/api/notifications/ \
  -H "Authorization: Token your_token_here"

# Mark notification as read
curl -X POST http://127.0.0.1:8000/api/notifications/1/mark-read/ \
  -H "Authorization: Token your_token_here"
Using Postman:
Set request method (GET, POST, PUT, PATCH, DELETE)

Set URL to appropriate endpoint

Add header: Authorization: Token <your_token>

Send request

ERROR HANDLING EXAMPLES
Duplicate Like Attempt:
json
{
  "error": "You have already liked this post"
}
Status: 400 Bad Request

Unlike Non-liked Post:
json
{
  "error": "You have not liked this post"
}
Status: 400 Bad Request

Unauthorized Notification Access:
json
{
  "error": "You do not have permission to mark this notification as read"
}
Status: 403 Forbidden

Resource Not Found:
json
{
  "error": "Post not found"
}
Status: 404 Not Found

