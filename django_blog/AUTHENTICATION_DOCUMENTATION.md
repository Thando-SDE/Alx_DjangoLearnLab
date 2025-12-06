# User Authentication System Documentation

## Overview
This Django blog project includes a comprehensive user authentication system with:
1. User registration
2. Login and logout
3. Profile management
4. Secure password handling

## Features

### 1. Registration
- Users can register with username, email, and password
- Email field is required and validated
- Passwords are securely hashed using Django's built-in PBKDF2 algorithm
- Success messages are displayed upon registration

### 2. Login/Logout
- Users can login with username and password
- Sessions are managed securely
- Logout clears the session
- CSRF protection is enabled on all forms

### 3. Profile Management
- Authenticated users can view and update their profile
- Users can change username and email
- Profile page is protected with login_required decorator

## Security Features
1. **CSRF Protection**: All forms include CSRF tokens
2. **Password Hashing**: Passwords are never stored in plain text
3. **Session Security**: Secure session management
4. **Input Validation**: All form inputs are validated

## How to Test

### 1. Registration Test
1. Navigate to `/register`
2. Fill in username, email, and password
3. Submit the form
4. Verify success message appears
5. Try to register with existing username (should show error)

### 2. Login Test
1. Navigate to `/login`
2. Enter credentials of registered user
3. Submit form
4. Verify user is redirected and navigation changes

### 3. Profile Test
1. Login first
2. Navigate to `/profile`
3. Update username or email
4. Submit changes
5. Verify success message appears

### 4. Logout Test
1. While logged in, click logout
2. Verify user is logged out and navigation changes

## File Structure
- `blog/forms.py`: Contains UserRegisterForm and UserUpdateForm
- `blog/views.py`: Contains authentication views
- `blog/templates/blog/`: Contains all authentication templates
- `blog/urls.py`: Contains URL patterns for authentication

## Dependencies
- Django 5.2.7 or higher
- Python 3.8 or higher
