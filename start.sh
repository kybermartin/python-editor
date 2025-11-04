#!/usr/bin/env bash
# Start script for Render — uses PORT env var if provided
if [ -z "$PORT" ]; then
  PORT=10000
fi
uvicorn main:app --host 0.0.0.0 --port $PORT
