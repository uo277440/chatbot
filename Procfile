release: python manage.py migrate
web: node server.js
daphne: daphne -b 0.0.0.0 -p $PORT chatbot.asgi:application



