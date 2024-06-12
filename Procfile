release: python manage.py migrate
backend: daphne -b 0.0.0.0 -p $PORT chatbot.asgi:application
web: sh -c 'cd chatfront && npm install && npm run build && cd .. && node server.js
