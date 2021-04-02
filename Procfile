release: python manage.py makemigrations --no-input
release: python manage.py migrate --no-input
release: python manage.py loaddata beach.json
web: gunicorn Surf_Backend.wsgi
