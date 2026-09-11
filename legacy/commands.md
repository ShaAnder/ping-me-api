uvicorn ping_me_api.asgi:application --port 8000 --workers 4 --log-level debug --reload

python3.11 -m venv venv
source venv/bin/activate