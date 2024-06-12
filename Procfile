release: python manage.py migrate
web: python manage.py collectstatic --noinput && daphne -b 0.0.0.0 -p $PORT chatbot.asgi:application
node: node server.js