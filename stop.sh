#!/bin/bash
cd "$(dirname "$0")"

echo "=========================================="
echo "Menghentikan Layanan ERPNext..."
echo "=========================================="

docker compose stop

echo "Layanan ERPNext berhasil dihentikan."
echo "Data Anda tetap tersimpan dengan aman di Docker volume."
echo "Jalankan ./start.sh untuk menyalakan kembali."
echo "=========================================="
