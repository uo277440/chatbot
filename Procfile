release: python manage.py migrate
web: gunicorn chatbot.wsgi
web: npm run build --prefix chatfront && python manage.py collectstatic --noinput && daphne -b 0.0.0.0 -p $PORT chatbot.asgi:application