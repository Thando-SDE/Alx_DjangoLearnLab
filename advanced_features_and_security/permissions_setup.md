# Permissions and Groups Setup

## Custom Permissions
Added to Book model in relationship_app:
- can_view: View books
- can_create: Create new books  
- can_edit: Edit existing books
- can_delete: Delete books

## Groups Created
- **Viewers**: can_view permission only
- **Editors**: can_view, can_create, can_edit permissions
- **Admins**: All permissions (can_view, can_create, can_edit, can_delete)

## Views Protected
- /books/ - requires can_view
- /books/create/ - requires can_create  
- /books/<id>/edit/ - requires can_edit
- /books/<id>/delete/ - requires can_delete

## Testing
1. Create test users in Django admin
2. Assign users to different groups
3. Test each URL endpoint to verify permissions work correctly
