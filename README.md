# ERPNext Local Environment - Hanifa Yulita ERP KELAS F

Direktori ini berisi konfigurasi lokal untuk menjalankan **ERPNext** menggunakan **Docker Desktop**.

---

## 🚀 Cara Mengakses ERPNext

Setelah instalasi selesai:
1. Buka browser (Chrome / Safari).
2. Kunjungi alamat: **[http://localhost:8080](http://localhost:8080)**
3. Masuk dengan akun default:
   - **Username**: `Administrator`
   - **Password**: `admin`

---

## 🕹️ Perintah Cepat (Shortcut)

Buka terminal di folder ini, lalu Anda dapat menjalankan:

- **Menyalakan ERPNext**:
  ```bash
  ./start.sh
  ```
- **Mematikan ERPNext** (ketika selesai kuliah/mengerjakan tugas agar hemat RAM):
  ```bash
  ./stop.sh
  ```
- **Mengecek Status Kontainer**:
  ```bash
  docker compose ps
  ```
- **Melihat Log**:
  ```bash
  docker compose logs -f
  ```

---

## 💾 Keamanan Data
Seluruh data database dan file yang Anda upload tersimpan di dalam **Docker Volumes** (`sites`, `db-data`, dll.), sehingga data tidak akan hilang saat komputer dimatikan atau saat kontainer dihentikan menggunakan `./stop.sh`.
