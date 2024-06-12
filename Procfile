release: python manage.py migrate
web: gunicorn chatbot.wsgi:application --bind 0.0.0.0:$PORT
worker: daphne -b 0.0.0.0 -p $PORT chatbot.asgi:application