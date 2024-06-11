release: python manage.py migrate
web: sh -c 'cd chatfront && npm install && npm run build && cd .. && python manage.py collectstatic --noinput && daphne -b 0.0.0.0 -p $PORT chatbot.asgi:application'