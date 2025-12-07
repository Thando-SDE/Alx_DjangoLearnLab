# Django Blog Project Documentation

## Project Overview
A complete Django blog application with advanced tagging and search functionality.

## Features
1. **Tagging System** - Posts can have multiple tags, tags are clickable
2. **Search Functionality** - Full-text search across titles, content, and tags
3. **User Authentication** - Registration, login, profile management
4. **Post Management** - Create, read, update, delete posts
5. **Comment System** - Authenticated users can comment on posts

## Setup
```bash
pip install django django-taggit
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
