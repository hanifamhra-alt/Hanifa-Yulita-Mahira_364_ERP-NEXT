import frappe

frappe.init(site='frontend')
frappe.connect()

print('='*85)
print('         REKAPITULASI BUKU BESAR & NERACA SALDO - PERUSAHAAN HANIRA PRIMA')
print('='*85)

gl_entries = frappe.db.sql("""
    SELECT 
        account,
        SUM(debit) as total_debit,
        SUM(credit) as total_credit,
        SUM(debit - credit) as net_balance
    FROM `tabGL Entry`
    WHERE is_cancelled = 0
    GROUP BY account
    ORDER BY account ASC
""", as_dict=True)

total_d = 0
total_c = 0

print(f"{'Kode & Nama Akun':<52} | {'Total Debit (Rp)':<16} | {'Total Kredit (Rp)':<16} | {'Saldo Akhir (Rp)':<18}")
print('-'*108)
for row in gl_entries:
    total_d += row.total_debit
    total_c += row.total_credit
    bal = row.net_balance
    bal_str = f"{bal:,.0f} (D)" if bal > 0 else (f"{abs(bal):,.0f} (K)" if bal < 0 else "0")
    print(f"{row.account:<52} | {row.total_debit:>16,.0f} | {row.total_credit:>16,.0f} | {bal_str:>18}")

print('-'*108)
print(f"{'TOTAL AKUMULATIF BUKU BESAR':<52} | {total_d:>16,.0f} | {total_c:>16,.0f} | {total_d - total_c:>18,.0f}")
if total_d == total_c:
    print('>>> STATUS KESEIMBANGAN: SEIMBANG / BALANCED (DEBIT = KREDIT) <<<')

print('\n' + '='*85)
print('                   POSISI PERSEDIAAN GUDANG (STOCK BALANCE)')
print('='*85)
bins = frappe.get_all('Bin', fields=['item_code', 'warehouse', 'actual_qty', 'valuation_rate', 'stock_value'])
for b in bins:
    if b.actual_qty > 0 or b.stock_value > 0:
        print(f"Item: {b.item_code:<14} | Gudang: {b.warehouse:<22} | Qty: {b.actual_qty:>4.0f} Nos | HPP: Rp {b.valuation_rate:>10,.0f} | Nilai Total: Rp {b.stock_value:>11,.0f}")

print('\n' + '='*85)
print('                     STATUS DOKUMEN & FAKTUR TRANSAKSI')
print('='*85)
for jv in frappe.get_all('Journal Entry', fields=['name', 'posting_date', 'total_debit', 'user_remark', 'docstatus']):
    print(f"Journal Entry   : {jv.name} | Tgl: {jv.posting_date} | Total: Rp {jv.total_debit:,.0f} | Remark: {jv.user_remark}")

for pi in frappe.get_all('Purchase Invoice', fields=['name', 'posting_date', 'supplier', 'grand_total', 'status', 'outstanding_amount']):
    print(f"Purchase Invoice: {pi.name} | Pemasok: {pi.supplier} | Total: Rp {pi.grand_total:,.0f} | Sisa: Rp {pi.outstanding_amount:,.0f} | Status: {pi.status}")

for se in frappe.get_all('Stock Entry', fields=['name', 'posting_date', 'purpose', 'total_outgoing_value', 'total_incoming_value']):
    print(f"Stock Entry     : {se.name} | Tipe: {se.purpose} | Out: Rp {se.total_outgoing_value:,.0f} | In: Rp {se.total_incoming_value:,.0f}")

for si in frappe.get_all('Sales Invoice', fields=['name', 'posting_date', 'customer', 'grand_total', 'status', 'outstanding_amount']):
    print(f"Sales Invoice   : {si.name} | Pelanggan: {si.customer} | Total: Rp {si.grand_total:,.0f} | Sisa: Rp {si.outstanding_amount:,.0f} | Status: {si.status}")

for pe in frappe.get_all('Payment Entry', fields=['name', 'posting_date', 'payment_type', 'party', 'paid_amount', 'status']):
    print(f"Payment Entry   : {pe.name} | Tipe: {pe.payment_type} | Pihak: {pe.party} | Nominal: Rp {pe.paid_amount:,.0f} | Status: {pe.status}")

print('\n' + '='*85)
print('                 LAPORAN LABA RUGI & POSISI KEUANGAN')
print('='*85)
penjualan = frappe.db.sql("SELECT SUM(credit - debit) FROM `tabGL Entry` WHERE account LIKE '41100%' AND is_cancelled=0")[0][0] or 0
hpp = frappe.db.sql("SELECT SUM(debit - credit) FROM `tabGL Entry` WHERE account LIKE '51100%' AND is_cancelled=0")[0][0] or 0
laba_kotor = penjualan - hpp
print(f"1. Pendapatan Penjualan (Sales)          : Rp {penjualan:>12,.0f}")
print(f"2. Harga Pokok Penjualan / HPP (COGS)    : Rp {hpp:>12,.0f}")
print(f"-----------------------------------------------------------------")
print(f"3. Laba Kotor Operasional (Gross Profit) : Rp {laba_kotor:>12,.0f}")

kas = frappe.db.sql("SELECT SUM(debit - credit) FROM `tabGL Entry` WHERE account LIKE '11110%' AND is_cancelled=0")[0][0] or 0
bank = frappe.db.sql("SELECT SUM(debit - credit) FROM `tabGL Entry` WHERE account LIKE '11120%' AND is_cancelled=0")[0][0] or 0
piutang = frappe.db.sql("SELECT SUM(debit - credit) FROM `tabGL Entry` WHERE account LIKE '11210%' AND is_cancelled=0")[0][0] or 0
persediaan_fg = frappe.db.sql("SELECT SUM(debit - credit) FROM `tabGL Entry` WHERE account LIKE '11340%' AND is_cancelled=0")[0][0] or 0
ppn_masukan = frappe.db.sql("SELECT SUM(debit - credit) FROM `tabGL Entry` WHERE account LIKE '11420%' AND is_cancelled=0")[0][0] or 0
total_aset = kas + bank + piutang + persediaan_fg + ppn_masukan

utang_usaha = frappe.db.sql("SELECT SUM(credit - debit) FROM `tabGL Entry` WHERE account LIKE '21110%' AND is_cancelled=0")[0][0] or 0
ppn_keluaran = frappe.db.sql("SELECT SUM(credit - debit) FROM `tabGL Entry` WHERE account LIKE '21310%' AND is_cancelled=0")[0][0] or 0
total_liabilitas = utang_usaha + ppn_keluaran

modal = frappe.db.sql("SELECT SUM(credit - debit) FROM `tabGL Entry` WHERE account LIKE '31000%' AND is_cancelled=0")[0][0] or 0
alokasi_btkl = frappe.db.sql("SELECT SUM(credit - debit) FROM `tabGL Entry` WHERE account LIKE '52100%' AND is_cancelled=0")[0][0] or 0
alokasi_bop = frappe.db.sql("SELECT SUM(credit - debit) FROM `tabGL Entry` WHERE account LIKE '53100%' AND is_cancelled=0")[0][0] or 0

print(f"\nPOSISI ASET:")
print(f" - Kas Operasional Pabrik                : Rp {kas:>12,.0f}")
print(f" - Bank Utama IDR                        : Rp {bank:>12,.0f}")
print(f" - Piutang Usaha                         : Rp {piutang:>12,.0f}")
print(f" - Persediaan Barang Jadi (2 unit @ 1.25M) : Rp {persediaan_fg:>12,.0f}")
print(f" - PPN Masukan (Klaim Pajak)             : Rp {ppn_masukan:>12,.0f}")
print(f" TOTAL ASET                              : Rp {total_aset:>12,.0f}")

print(f"\nPOSISI KEWAJIBAN & EKUITAS:")
print(f" - Utang Dagang Pemasok                  : Rp {utang_usaha:>12,.0f}")
print(f" - Utang PPN Keluaran                    : Rp {ppn_keluaran:>12,.0f}")
print(f" - Modal Disetor Pemegang Saham          : Rp {modal:>12,.0f}")
print(f" - Laba Bersih Tahun Berjalan            : Rp {laba_kotor + alokasi_btkl + alokasi_bop:>12,.0f}")
print(f" TOTAL KEWAJIBAN + EKUITAS               : Rp {total_liabilitas + modal + laba_kotor + alokasi_btkl + alokasi_bop:>12,.0f}")

frappe.destroy()
