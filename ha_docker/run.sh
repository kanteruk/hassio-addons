#!/usr/bin/env bash
set -e

echo "RF Addon started (Ubuntu 22.04 + Python)"
echo "Python version:"
python3 --version

export PATH="/opt/venv/bin:$PATH"

echo "Starting RF Addon FastAPI + Playwright..."
PORT="${PORT:-8080}"

exec uvicorn main:app --host 0.0.0.0 --port $PORT
