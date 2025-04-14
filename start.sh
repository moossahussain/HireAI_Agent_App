#!/bin/bash

echo " Starting FastAPI (Uvicorn)..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 > uvicorn.log 2>&1 &

echo " Uvicorn running in background"

# Optional delay to give backend time to boot before Nginx
sleep 5

echo " Starting Nginx (foreground)..."
exec nginx -g "daemon off;"
