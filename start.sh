#!/bin/bash
cd "$(dirname "$0")"

echo "=========================================="
echo "Menjalankan Layanan ERPNext..."
echo "=========================================="

docker compose up -d

echo ""
echo "ERPNext sedang berjalan di latar belakang."
echo "Buka di browser: http://localhost:8080"
echo "Username: Administrator"
echo "Password: admin"
echo "=========================================="
