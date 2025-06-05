#!/bin/sh

./wait-for-it.sh postgres_db:5432 -- alembic upgrade head

echo "Starting backend..."
python3 db_entrypoint.py
exec uvicorn app:fast_api_app --host 0.0.0.0 --port 9000
