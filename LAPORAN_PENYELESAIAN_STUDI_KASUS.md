# LAPORAN PENYELESAIAN STUDI KASUS MANUFAKTUR ERPNEXT
**Mata Kuliah**: Sistem Enterprise / ERP (Kelas F)  
**Nama Entitas**: Hanira Prima (PT TechnoFab Manufaktur Indonesia)  
**Produk Kasus**: Solar Power Inverter 1000W (`FG-INV-1000`)  
**Status Eksekusi**: ✅ **100% Selesai & Terverifikasi di ERPNext (http://localhost:8080)**

---

## 1. PENDAHULUAN & RUANG LINGKUP
Studi kasus ini mensimulasikan proses operasional dan akuntansi industri manufaktur pengolahan perakitan inverter tenaga surya secara terintegrasi (End-to-End) menggunakan ERPNext. Seluruh transaksi telah dieksekusi secara nyata ke dalam basis data ERPNext pada entitas **Hanira Prima (HP)** yang merujuk pada standar hierarki 72 akun di `COA_Manufaktur.xlsx`.

---

## 2. MASTER DATA YANG DIBENTUK DI SISTEM
| Kategori Master | Kode / Nama | Tipe / Grup | Nilai Standar (Rp) | Keterangan |
| :--- | :--- | :--- | :--- | :--- |
| **Gudang (Warehouse)** | `Stores - HP` | Stores | - | Akun: `11310 - Persediaan Bahan Baku` |
| | `Work In Progress - HP` | WIP | - | Akun: `11330 - Persediaan WIP` |
| | `Finished Goods - HP` | Finished Goods | - | Akun: `11340 - Persediaan Barang Jadi` |
| **Bahan Baku (Raw Material)** | `RM-PCB-001` | PCB Assembly Control Board | Rp 300.000 / Nos | Bahan baku utama kontrol sirkuit |
| | `RM-ALU-002` | Aluminium Casing Enclosure | Rp 150.000 / Nos | Casing dan pelindung mekanis |
| | `RM-TRF-003` | Copper Transformer 1kVA | Rp 450.000 / Nos | Transformator daya tembaga murni |
| | `RM-FET-004` | Power MOSFET Set | Rp 25.000 / Nos | Komponen pensaklaran daya tinggi (x4) |
| **Barang Jadi (Finished Good)**| `FG-INV-1000` | Solar Power Inverter 1000W | Rp 2.000.000 / Nos | Harga Jual Standar (HPP Standar: Rp 1.250.000) |
| **Bill of Materials (BOM)** | `BOM-FG-INV-1000-001`| BOM Standar 1 Unit | Rp 1.250.000 / Unit | Rincian Bahan (Rp 1M) + BTKL (150rb) + BOP (100rb) |
| **Mitra Bisnis Pemasok** | `PT Komponen Utama Pemasok` | Supplier (Raw Material) | - | Vendor penyedia 4 komponen bahan baku |
| **Mitra Bisnis Pelanggan** | `PT Surya Energi Indonesia` | Customer (Commercial) | - | Distributor pembeli inverter tenaga surya |

---

## 3. LOG EKSEKUSI & REKAP TRANSAKSI (TX-001 s/d TX-006)

### [TX-001] Setoran Modal Awal Pemilik Saham
- **Nomor Dokumen ERPNext**: `ACC-JV-2026-00001`
- **Tipe Dokumen**: Journal Entry (Submitted)
- **Keterangan**: Penerimaan uang tunai setoran modal awal ke brankas/kas operasional pabrik.
- **Dampak Jurnal Akuntansi**:
  - `(Debet)  11110 - Kas Kecil Pabrik (Factory Petty Cash) - HP` : **Rp 100.000.000**
  - `(Kredit) 31000 - Modal Disetor (Paid-in Capital) - HP`         : **Rp 100.000.000**

---

### [TX-002] Pembelian 10 Set Bahan Baku Lengkap (+ PPN Masukan 11%)
- **Nomor Dokumen ERPNext**: `ACC-PINV-2026-00001`
- **Tipe Dokumen**: Purchase Invoice (Update Stock = 1, Submitted, Status: Paid)
- **Pemasok**: PT Komponen Utama Pemasok
- **Rincian Barang**:
  1. `RM-PCB-001`: 10 Nos @ Rp 300.000 = Rp 3.000.000
  2. `RM-ALU-002`: 10 Nos @ Rp 150.000 = Rp 1.500.000
  3. `RM-TRF-003`: 10 Nos @ Rp 450.000 = Rp 4.500.000
  4. `RM-FET-004`: 40 Nos @ Rp 25.000 = Rp 1.000.000
- **Total Pembelian DPP**: Rp 10.000.000 | **PPN Masukan (11%)**: Rp 1.100.000 | **Total Tagihan**: Rp 11.100.000
- **Dampak Jurnal Akuntansi**:
  - `(Debet)  11310 - Persediaan Bahan Baku - HP`                      : **Rp 10.000.000**
  - `(Debet)  11420 - PPN Masukan (VAT Inward) - HP`                   : **Rp 1.100.000**
  - `(Kredit) 21110 - Utang Dagang Pemasok Bahan Baku - HP`            : **Rp 11.100.000**

---

### [TX-003] Transfer Bahan Baku ke Lantai Produksi (Material Transfer to WIP)
- **Nomor Dokumen ERPNext**: `MAT-STE-2026-00001`
- **Tipe Dokumen**: Stock Entry (Material Transfer for Manufacture, Submitted)
- **Rute Perpindahan**: Dari `Stores - HP` ke `Work In Progress - HP` (10 set lengkap)
- **Total Nilai Bahan Ditransfer**: Rp 10.000.000
- **Dampak Jurnal Akuntansi**:
  - `(Debet)  11330 - Persediaan Barang Dalam Proses (WIP) - HP`        : **Rp 10.000.000**
  - `(Kredit) 11310 - Persediaan Bahan Baku - HP`                      : **Rp 10.000.000**

---

### [TX-004] Proses Pabrikasi 10 Unit Inverter & Pembebanan Biaya Konversi (Manufacture)
- **Nomor Dokumen ERPNext**: `MAT-STE-2026-00002`
- **Tipe Dokumen**: Stock Entry (Manufacture, Submitted)
- **BOM Digunakan**: `BOM-FG-INV-1000-001` | **Barang Dihasilkan**: 10 unit `FG-INV-1000`
- **Alokasi Biaya Tambahan Operasional (Conversion Costs)**:
  - Alokasi Upah Langsung (BTKL): Rp 1.500.000 (`52100 - Upah & Gaji Buruh Produksi`)
  - Alokasi Overhead Pabrik (BOP): Rp 1.000.000 (`53100 - Pemakaian Bahan Penolong / BOP`)
- **Total Nilai Barang Jadi Masuk Gudang**: Rp 10.000.000 (Material) + Rp 2.500.000 (Konversi) = **Rp 12.500.000** (Rp 1.250.000 / unit)
- **Dampak Jurnal Akuntansi**:
  - `(Debet)  11340 - Persediaan Barang Jadi (Finished Goods) - HP`   : **Rp 12.500.000**
  - `(Kredit) 11330 - Persediaan Barang Dalam Proses (WIP) - HP`       : **Rp 10.000.000**
  - `(Kredit) 52100 - Upah & Gaji Buruh Produksi (BTKL) - HP`         : **Rp 1.500.000**
  - `(Kredit) 53100 - Pemakaian Bahan Penolong (BOP) - HP`            : **Rp 1.000.000**

---

### [TX-005] Penjualan & Pengiriman 8 Unit Inverter (+ PPN Keluaran 11%)
- **Nomor Dokumen ERPNext**: `ACC-SINV-2026-00001`
- **Tipe Dokumen**: Sales Invoice (Update Stock = 1, Submitted, Status: Paid)
- **Pelanggan**: PT Surya Energi Indonesia
- **Kuantitas & Harga**: 8 unit `FG-INV-1000` @ Rp 2.000.000 = Rp 16.000.000
- **PPN Keluaran (11%)**: Rp 1.760.000 | **Total Tagihan Piutang**: **Rp 17.760.000**
- **Pengakuan HPP Barang Terjual**: 8 unit x Rp 1.250.000 = **Rp 10.000.000**
- **Dampak Jurnal Akuntansi**:
  - `(Debet)  11210 - Piutang Dagang Pelanggan - HP`                   : **Rp 17.760.000**
  - `(Debet)  51100 - Pemakaian Bahan Baku Utama (HPP) - HP`           : **Rp 10.000.000**
  - `(Kredit) 41100 - Penjualan Barang Jadi - Domestik - HP`          : **Rp 16.000.000**
  - `(Kredit) 21310 - PPN Keluaran (VAT Outward) - HP`                : **Rp 1.760.000**
  - `(Kredit) 11340 - Persediaan Barang Jadi (Finished Goods) - HP`   : **Rp 10.000.000**

---

### [TX-006] Penerimaan Pembayaran Pelanggan & Pelunasan Utang Pemasok
- **Nomor Dokumen ERPNext**:
  1. `ACC-PAY-2026-00001` (Receive): Pelunasan Piutang dari PT Surya Energi Indonesia
  2. `ACC-PAY-2026-00002` (Pay): Pembayaran Utang ke PT Komponen Utama Pemasok
- **Dampak Jurnal Akuntansi**:
  - *Pelunasan Piutang*:
    - `(Debet)  11120 - Bank Utama IDR (Main Bank Account) - HP`      : **Rp 17.760.000**
    - `(Kredit) 11210 - Piutang Dagang Pelanggan - HP`                 : **Rp 17.760.000**
  - *Pembayaran Utang*:
    - `(Debet)  21110 - Utang Dagang Pemasok Bahan Baku - HP`          : **Rp 11.100.000**
    - `(Kredit) 11120 - Bank Utama IDR (Main Bank Account) - HP`      : **Rp 11.100.000**

---

## 4. NERACA SALDO AKHIR SISTEM (TRIAL BALANCE)
Berdasarkan pembacaan langsung dari tabel `tabGL Entry` ERPNext:

| Kode & Nama Akun | Debet Kumulatif (Rp) | Kredit Kumulatif (Rp) | Saldo Akhir Neraca Saldo (Rp) |
| :--- | :---: | :---: | :---: |
| `11110 - Kas Kecil Pabrik (Factory Petty Cash) - HP` | 100.000.000 | 0 | **100.000.000 (D)** |
| `11120 - Bank Utama IDR (Main Bank Account) - HP` | 17.760.000 | 11.100.000 | **6.660.000 (D)** |
| `11210 - Piutang Dagang Pelanggan - HP` | 17.760.000 | 17.760.000 | **0 (Lunas)** |
| `11310 - Persediaan Bahan Baku - HP` | 10.000.000 | 10.000.000 | **0 (Habis Terpakai)** |
| `11330 - Persediaan Barang Dalam Proses (WIP) - HP` | 10.000.000 | 10.000.000 | **0 (Tuntas Dirakit)** |
| `11340 - Persediaan Barang Jadi - HP` | 12.500.000 | 10.000.000 | **2.500.000 (D) [2 Unit]** |
| `11420 - PPN Masukan (VAT Inward) - HP` | 1.100.000 | 0 | **1.100.000 (D)** |
| `21110 - Utang Dagang Pemasok - HP` | 11.100.000 | 11.100.000 | **0 (Lunas)** |
| `21310 - PPN Keluaran (VAT Outward) - HP` | 0 | 1.760.000 | **1.760.000 (K)** |
| `31000 - Modal Disetor (Paid-in Capital) - HP` | 0 | 100.000.000 | **100.000.000 (K)** |
| `41100 - Penjualan Barang Jadi - Domestik - HP` | 0 | 16.000.000 | **16.000.000 (K)** |
| `51100 - Pemakaian Bahan Baku Utama (HPP) - HP` | 10.000.000 | 0 | **10.000.000 (D)** |
| `52100 - Upah & Gaji Buruh Produksi (BTKL) - HP` | 0 | 1.500.000 | **1.500.000 (K)** |
| `53100 - Pemakaian Bahan Penolong (BOP) - HP` | 0 | 1.000.000 | **1.000.000 (K)** |
| **TOTAL KESELURUHAN (BALANCE CHECK)** | **190.220.000** | **190.220.000** | **SELISIH = Rp 0 (SEIMBANG)** |

---

## 5. POSISI KARTU STOK FISIK (STOCK LEDGER / BALANCE)
| Kode Item | Nama Item | Gudang | Kuantitas Awal | Masuk | Keluar | Sisa Akhir | HPP / Unit | Nilai Akhir Gudang |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `RM-PCB-001` | PCB Control Board | Stores | 0 | 10 | 10 | **0 Nos** | Rp 300.000 | Rp 0 |
| `RM-ALU-002` | Casing Enclosure | Stores | 0 | 10 | 10 | **0 Nos** | Rp 150.000 | Rp 0 |
| `RM-TRF-003` | Transformer 1kVA | Stores | 0 | 10 | 10 | **0 Nos** | Rp 450.000 | Rp 0 |
| `RM-FET-004` | Power MOSFET Set | Stores | 0 | 40 | 40 | **0 Nos** | Rp 25.000 | Rp 0 |
| `FG-INV-1000` | Inverter 1000W | Finished Goods | 0 | 10 | 8 | **2 Nos** | **Rp 1.250.000** | **Rp 2.500.000** |

---

## 6. LAPORAN KEUANGAN AKHIR (FINANCIAL STATEMENTS)

### A. Laporan Laba Rugi (Income Statement)
| Deskripsi Akun | Nominal (Rp) |
| :--- | :--- |
| **Pendapatan Usaha Penjualan** (8 unit @ Rp 2.000.000) | Rp 16.000.000 |
| **Beban Pokok Penjualan (HPP)** (8 unit @ Rp 1.250.000) | (Rp 10.000.000) |
| **Laba Kotor Operasional (Gross Profit)** | **Rp 6.000.000** |
| Kredit Penyerapan Biaya Konversi Produksi (BTKL & BOP diserap ke stok) | Rp 2.500.000 |
| **Laba Bersih Tahun Berjalan (Net Profit)** | **Rp 8.500.000** |

### B. Neraca / Laporan Posisi Keuangan (Balance Sheet)
| ASET | Nominal (Rp) | KEWAJIBAN & EKUITAS | Nominal (Rp) |
| :--- | :--- | :--- | :--- |
| **Kas Operasional Pabrik** | Rp 100.000.000 | **Utang Dagang Pemasok** | Rp 0 |
| **Bank Utama IDR** | Rp 6.660.000 | **Utang PPN Keluaran** | Rp 1.760.000 |
| **Piutang Usaha Pelanggan** | Rp 0 | *Total Kewajiban* | *Rp 1.760.000* |
| **Persediaan Barang Jadi (2 unit)**| Rp 2.500.000 | **Modal Disetor Saham** | Rp 100.000.000 |
| **PPN Masukan (Uang Muka Pajak)** | Rp 1.100.000 | **Laba Tahun Berjalan** | Rp 8.500.000 |
| | | *Total Ekuitas* | *Rp 108.500.000* |
| **TOTAL ASET** | **Rp 110.260.000** | **TOTAL LIABILITAS + EKUITAS** | **Rp 110.260.000** |

*(Kondisi Neraca: **Aset (Rp 110.260.000) = Liabilitas + Ekuitas (Rp 110.260.000)**)*

---

## 7. CARA MENGECEK LANGSUNG DI BROWSER
Bagi Anda atau Dosen Penguji yang ingin memeriksa langsung hasil pekerjaan ini di antarmuka ERPNext:
1. Buka browser: **[http://localhost:8080](http://localhost:8080)**
2. Login: **Administrator** | Password: **admin**
3. Akses modul berikut:
   - **Accounting > General Ledger**: Filter Company `Hanira Prima` untuk melihat jurnal buku besar lengkap yang seimbang.
   - **Accounting > Trial Balance**: Untuk melihat Neraca Saldo Rp 190.220.000 (Balance).
   - **Stock > Stock Balance**: Untuk melihat 2 unit Solar Inverter di gudang `Finished Goods - HP`.
   - **Buying > Purchase Invoice**: Melihat faktur `ACC-PINV-2026-00001` berstatus *Paid*.
   - **Selling > Sales Invoice**: Melihat faktur `ACC-SINV-2026-00001` berstatus *Paid*.
