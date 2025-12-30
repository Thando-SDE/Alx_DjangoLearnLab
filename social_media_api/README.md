# Social Media REST API

A fully-featured Django REST API for a social media platform with authentication, posts, comments, likes, follows, and real-time notifications.

## 🚀 Features

- **User Authentication** (Register, Login, JWT Tokens)
- **User Profiles** with bio and profile pictures
- **Posts** with title, content, and images
- **Comments** on posts
- **Likes** on posts
- **User Follows/Unfollows**
- **Personalized Feed** (posts from followed users)
- **Real-time Notifications** for likes, comments, and follows
- **RESTful API** with proper HTTP methods and status codes
- **Production-ready** with security best practices

## 📋 API Documentation

Complete API documentation is available in [API_DOCUMENTATION.md](API_DOCUMENTATION.md).

### Key Endpoints:
- `POST /api/accounts/register/` - Register new user
- `POST /api/accounts/login/` - Login user
- `GET /api/accounts/profile/` - Get user profile
- `GET /api/posts/` - List/Create posts
- `POST /api/posts/<id>/like/` - Like a post
- `POST /api/accounts/follow/<user_id>/` - Follow a user
- `GET /api/feed/` - Get personalized feed
- `GET /api/notifications/` - Get user notifications

## 🛠️ Tech Stack

- **Backend:** Django 5.2.7 + Django REST Framework
- **Database:** PostgreSQL (production), SQLite (development)
- **Authentication:** Token Authentication
- **Static Files:** WhiteNoise + AWS S3 (optional)
- **Deployment:** Heroku-ready with Gunicorn
- **Security:** HTTPS, CORS, XSS protection, HSTS

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd social_media_api
```

### 2. Set Up Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
```bash
cp .env.example .env
# Edit .env with your settings
```

### 5. Run Migrations
```bash
python manage.py migrate
```

### 6. Create Superuser
```bash
python manage.py createsuperuser
```

### 7. Run Development Server
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

## 🔧 Configuration

### Environment Variables
See `.env.example` for all available environment variables:

```bash
# Django
SECRET_KEY=your-secret-key
DEBUG=True  # Set to False in production
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (PostgreSQL for production)
DATABASE_URL=postgres://user:password@localhost:5432/dbname

# AWS S3 (optional, for production static files)
USE_S3=False
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_STORAGE_BUCKET_NAME=your-bucket
```

## 🚢 Deployment

### Heroku Deployment
```bash
# 1. Install Heroku CLI and login
heroku login

# 2. Create Heroku app
heroku create your-app-name

# 3. Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# 4. Set environment variables
heroku config:set SECRET_KEY=$(python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
heroku config:set DEBUG=False

# 5. Deploy
git push heroku main

# 6. Run migrations
heroku run python manage.py migrate
```

### Other Platforms
The application is also configured for:
- **Railway.app**
- **Render.com**
- **AWS Elastic Beanstalk**
- **DigitalOcean**
- **PythonAnywhere**

## 📁 Project Structure

```
social_media_api/
├── accounts/           # User authentication & profiles
│   ├── models.py      # CustomUser model
│   ├── views.py       # Auth views
│   ├── serializers.py # User serializers
│   └── urls.py        # Auth endpoints
├── posts/             # Posts, comments, likes
│   ├── models.py      # Post, Comment, Like models
│   ├── views.py       # Post views + feed
│   ├── serializers.py # Post serializers
│   └── urls.py        # Post endpoints
├── notifications/     # Real-time notifications
│   ├── models.py      # Notification model
│   ├── views.py       # Notification views
│   ├── signals.py     # Signal handlers
│   └── urls.py        # Notification endpoints
├── social_media_api/  # Project settings
│   └── settings.py    # Production-ready settings
├── requirements.txt   # Production dependencies
├── Procfile          # Heroku process definition
├── runtime.txt       # Python version
├── deploy.sh         # Deployment script
├── .env.example      # Environment template
└── API_DOCUMENTATION.md # Complete API docs
```

## 🔒 Security

The API includes:
- HTTPS enforcement in production
- CORS configuration
- XSS protection headers
- HSTS preloading
- Secure cookies
- SQL injection protection
- Password validation
- Token authentication

## 🧪 Testing

Run the development server and test endpoints using:
- **Web Interface:** `http://localhost:8000/api/`
- **API Clients:** Postman, Insomnia, or curl
- **Admin Panel:** `http://localhost:8000/admin/`

## 📄 License

This project is for educational purposes as part of the ALX Django Learning Lab.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📞 Support

For issues or questions, please check the API documentation or open an issue in the repository.
