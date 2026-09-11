release: python manage.py makemigrations && python manage.py migrate
web: daphne ping_me_api.asgi:application --bind 0.0.0.0 --port ${PORT}