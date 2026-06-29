#!/bin/bash
echo "Starting Cloudflare Quick Tunnel for n8n..."
# Run in background, log output to tunnel.log
cloudflared tunnel --url http://localhost:5678 > tunnel.log 2>&1 &
PID=$!
echo "Tunnel process started with PID $PID"
sleep 5
# Grep for the trycloudflare URL
URL=$(grep -oE "https://[a-zA-Z0-9-]+\.trycloudflare\.com" tunnel.log | head -n 1)
if [ -n "$URL" ]; then
  echo "=============================================="
  echo "SUCCESS: Your tunnel is active!"
  echo "n8n Webhook URL: $URL/webhook/omi-webhook"
  echo "=============================================="
else
  echo "Waiting for tunnel URL to generate..."
  sleep 5
  URL=$(grep -oE "https://[a-zA-Z0-9-]+\.trycloudflare\.com" tunnel.log | head -n 1)
  if [ -n "$URL" ]; then
    echo "=============================================="
    echo "SUCCESS: Your tunnel is active!"
    echo "n8n Webhook URL: $URL/webhook/omi-webhook"
    echo "=============================================="
  else
    echo "Could not extract tunnel URL. Check tunnel.log:"
    cat tunnel.log
  fi
fi
