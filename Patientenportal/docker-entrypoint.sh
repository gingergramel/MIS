#!/bin/bash
set -e

echo "Running Django migrations..."
python manage.py makemigrations
python manage.py migrate

echo "Starting Django application..."
python -m uvicorn --host 0.0.0.0 --port 8000 mysite.asgi:application