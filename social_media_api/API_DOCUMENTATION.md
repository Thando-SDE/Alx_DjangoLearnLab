# Social Media API Documentation
## Posts and Comments Endpoints

### Authentication
All endpoints require token authentication except where noted.
Include token in request header:

Authorization: Token <your_token>

### Base URL
`http://127.0.0.1:8000/api/`

---

## POSTS ENDPOINTS

### 1. List All Posts
**GET** `/posts/`

**Query Parameters:**
- `page` (optional): Page number for pagination (default: 1)
- `page_size` (optional): Items per page (default: 10, max: 100)
- `search` (optional): Search in title or content
- `author` (optional): Filter by author ID

**Response (200 OK):**
```json
{
  "count": 2,
  "next": "http://127.0.0.1:8000/api/posts/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "author": 4,
      "author_username": "testuser3",
      "title": "My First Post",
      "content": "Post content",
      "created_at": "2025-12-21T05:14:01.151891Z",
      "updated_at": "2025-12-21T05:14:01.151891Z"
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
  "author": 4,
  "author_username": "testuser3",
  "title": "Post Title",
  "content": "Post content here",
  "created_at": "2025-12-21T05:20:01.151891Z",
  "updated_at": "2025-12-21T05:20:01.151891Z"
}
3. Retrieve a Single Post
GET /posts/{id}/

Response (200 OK):

json
{
  "id": 1,
  "author": 4,
  "author_username": "testuser3",
  "title": "My First Post",
  "content": "Post content",
  "created_at": "2025-12-21T05:14:01.151891Z",
  "updated_at": "2025-12-21T05:14:01.151891Z"
}
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

COMMENTS ENDPOINTS
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
  "author": 4,
  "author_username": "testuser3",
  "content": "This is a comment",
  "created_at": "2025-12-21T05:25:01.151891Z",
  "updated_at": "2025-12-21T05:25:01.151891Z"
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

AUTHENTICATION ENDPOINTS (from Task 0)
Register User
POST /api/accounts/register/

Request Body:

json
{
  "username": "newuser",
  "email": "user@example.com",
  "password": "password123"
}
Login
POST /api/accounts/login/

Request Body:

json
{
  "username": "newuser",
  "password": "password123"
}
Get User Profile
GET /api/accounts/profile/