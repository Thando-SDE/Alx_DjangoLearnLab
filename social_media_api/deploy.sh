#!/bin/bash
# Deployment script for Social Media API

set -e  # Exit on error

echo "🚀 Starting deployment process..."
echo "================================="

echo ""
echo "1. Installing Python dependencies..."
pip install -r requirements.txt

echo ""
echo "2. Collecting static files..."
python manage.py collectstatic --noinput

echo ""
echo "3. Applying database migrations..."
python manage.py migrate

echo ""
echo "✅ Deployment preparation complete!"
echo ""
echo "Next steps:"
echo "- Configure environment variables"
echo "- Start the server: gunicorn social_media_api.wsgi:application"
echo "- Or run in development: python manage.py runserver"
