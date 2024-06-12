release: python manage.py migrate
web: sh -c 'cd chatfront && npm install && npm run build && cd .. && python manage.py collectstatic --noinput && gunicorn chatbot.wsgi:application --bind 0.0.0.0:$PORT'
daphne: daphne -b 0.0.0.0 -p $PORT chatbot.asgi:application