#!/usr/bin/env bash

echo "RF Addon started (Ubuntu 22.04 + Python)"
echo "Python version:"
python3 --version

set -e

# Вказуємо порт FastAPI з конфігурації аддону або дефолт
PORT="${PORT:-8000}"

# Запуск FastAPI
exec uvicorn main:app --host 0.0.0.0 --port $PORT

