FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the app code into /app/game_app
COPY game_app ./game_app

# Optionally copy migrations into /app/migrations
COPY migrations ./migrations

COPY README.md .

CMD sh -c 'gunicorn -b 0.0.0.0:${PORT:-8000} "game_app.core:create_app()"'
