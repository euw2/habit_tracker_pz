# This file is an entry point for development environment
sleep 10
python manage.py migrate
python manage.py runserver 0.0.0.0:8000