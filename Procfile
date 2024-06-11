release: python manage.py migrate
web: gunicorn chatbot.wsgi
web: daphne -b 0.0.0.0 -p $PORT chatbot.asgi:application