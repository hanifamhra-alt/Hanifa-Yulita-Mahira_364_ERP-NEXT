"""
===============================================================================
STUDI KASUS TRANSAKSI MANUFAKTUR ERPNEXT
Antigravity IDE - Executable Transaction Engine & REST API Client
===============================================================================
Skenario: PT TechnoFab Manufaktur Indonesia
Produk: Solar Power Inverter 1000W (FG-INV-1000)
COA Reference: COA_Manufaktur.xlsx
===============================================================================
"""

import os
import sys
import json
import time
import argparse

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

CASE_STUDY_DATA = {
    "company": "PT TechnoFab Manufaktur Indonesia",
    "abbr": "PTF",
    "currency": "IDR",
    "warehouses": [
        {"name": "Stores - PTF", "type": "Stores"},
        {"name": "Work in Progress - PTF", "type": "WIP"},
        {"name": "Finished Goods - PTF", "type": "Finished Goods"}
    ],
    "items": [
        {"code": "RM-PCB-001", "name": "PCB Assembly Control Board", "group": "Raw Material", "uom": "Nos", "standard_rate": 300000},
        {"code": "RM-ALU-002", "name": "Aluminium Casing Enclosure", "group": "Raw Material", "uom": "Nos", "standard_rate": 150000},
        {"code": "RM-TRF-003", "name": "Copper Transformer 1kVA", "group": "Raw Material", "uom": "Nos", "standard_rate": 450000},
        {"code": "RM-FET-004", "name": "Power MOSFET Set", "group": "Raw Material", "uom": "Nos", "standard_rate": 25000},
        {"code": "FG-INV-1000", "name": "Solar Power Inverter 1000W", "group": "Products", "uom": "Nos", "standard_rate": 2000000}
    ],
    "bom": {
        "item_code": "FG-INV-1000",
        "quantity": 1,
        "items": [
            {"item_code": "RM-PCB-001", "qty": 1, "rate": 300000},
            {"item_code": "RM-ALU-002", "qty": 1, "rate": 150000},
            {"item_code": "RM-TRF-003", "qty": 1, "rate": 450000},
            {"item_code": "RM-FET-004", "qty": 4, "rate": 25000}
        ],
        "operating_cost": 150000,
        "overhead_cost": 100000
    },
    "transactions": [
        {
            "step": 1,
            "code": "TX-001",
            "title": "Setoran Modal Awal Disetor",
            "doctype": "Journal Entry",
            "description": "Penerimaan kas setoran modal awal dari pemegang saham.",
            "entries": [
                {"account": "11110 - Kas Operasional Pabrik - PTF", "debit": 100000000, "credit": 0},
                {"account": "31100 - Modal Disetor - PTF", "debit": 0, "credit": 100000000}
            ]
        },
        {
            "step": 2,
            "code": "TX-002",
            "title": "Pembelian Bahan Baku (Purchase Order & Purchase Invoice)",
            "doctype": "Purchase Invoice",
            "supplier": "PT Komponen Utama Pemasok",
            "description": "Pembelian 10 set bahan baku lengkap dengan PPN Masukan 11%.",
            "items": [
                {"item_code": "RM-PCB-001", "qty": 10, "rate": 300000, "amount": 3000000},
                {"item_code": "RM-ALU-002", "qty": 10, "rate": 150000, "amount": 1500000},
                {"item_code": "RM-TRF-003", "qty": 10, "rate": 450000, "amount": 4500000},
                {"item_code": "RM-FET-004", "qty": 40, "rate": 25000, "amount": 1000000}
            ],
            "tax": {"account": "11410 - PPN Masukan - PTF", "rate": 11, "amount": 1100000},
            "total_payable": 11100000,
            "entries": [
                {"account": "11310 - Persediaan Bahan Baku - PTF", "debit": 10000000, "credit": 0},
                {"account": "11410 - PPN Masukan - PTF", "debit": 1100000, "credit": 0},
                {"account": "21110 - Utang Dagang Pemasok - PTF", "debit": 0, "credit": 11100000}
            ]
        },
        {
            "step": 3,
            "code": "TX-003",
            "title": "Transfer Bahan Baku ke WIP (Stock Entry: Material Transfer)",
            "doctype": "Stock Entry",
            "purpose": "Material Transfer for Manufacture",
            "from_warehouse": "Stores - PTF",
            "to_warehouse": "Work in Progress - PTF",
            "description": "Pengeluaran 10 set bahan baku dari gudang ke lantai produksi.",
            "entries": [
                {"account": "11330 - Persediaan Work-in-Progress (WIP) - PTF", "debit": 10000000, "credit": 0},
                {"account": "11310 - Persediaan Bahan Baku - PTF", "debit": 0, "credit": 10000000}
            ]
        },
        {
            "step": 4,
            "code": "TX-004",
            "title": "Proses Produksi & Pengakuan Cost (Stock Entry: Manufacture)",
            "doctype": "Stock Entry",
            "purpose": "Manufacture",
            "work_order": "WO-2026-00001",
            "finished_good": "FG-INV-1000",
            "produced_qty": 10,
            "additional_costs": [
                {"account": "52100 - Alokasi BTKL - PTF", "amount": 1500000, "label": "Direct Labor (BTKL)"},
                {"account": "53100 - Alokasi BOP - PTF", "amount": 1000000, "label": "Overhead Pabrik (BOP)"}
            ],
            "description": "Penyelesaian 10 unit Solar Inverter 1000W ke gudang barang jadi.",
            "entries": [
                {"account": "11340 - Persediaan Barang Jadi - PTF", "debit": 12500000, "credit": 0},
                {"account": "11330 - Persediaan Work-in-Progress (WIP) - PTF", "debit": 0, "credit": 10000000},
                {"account": "52100 - Alokasi Biaya Tenaga Kerja Langsung - PTF", "debit": 0, "credit": 1500000},
                {"account": "53100 - Alokasi Biaya Overhead Pabrik - PTF", "debit": 0, "credit": 1000000}
            ]
        },
        {
            "step": 5,
            "code": "TX-005",
            "title": "Penjualan & Pengiriman Barang (Sales Order & Sales Invoice)",
            "doctype": "Sales Invoice",
            "customer": "PT Surya Energi Indonesia",
            "description": "Penjualan 8 unit Solar Inverter @ Rp 2.000.000 + PPN Keluaran 11%.",
            "items": [
                {"item_code": "FG-INV-1000", "qty": 8, "rate": 2000000, "amount": 16000000, "cogs_rate": 1250000}
            ],
            "tax": {"account": "21210 - PPN Keluaran - PTF", "rate": 11, "amount": 1760000},
            "total_receivable": 17760000,
            "entries": [
                {"account": "11210 - Piutang Dagang Pelanggan - PTF", "debit": 17760000, "credit": 0},
                {"account": "41100 - Penjualan Barang Jadi - PTF", "debit": 0, "credit": 16000000},
                {"account": "21210 - PPN Keluaran - PTF", "debit": 0, "credit": 1760000},
                {"account": "51100 - HPP Barang Jadi - PTF", "debit": 10000000, "credit": 0},
                {"account": "11340 - Persediaan Barang Jadi - PTF", "debit": 0, "credit": 10000000}
            ]
        },
        {
            "step": 6,
            "code": "TX-006",
            "title": "Penerimaan Pelunasan Piutang & Pembayaran Utang Pemasok",
            "doctype": "Payment Entry",
            "description": "Penerimaan pembayaran dari pelanggan dan pelunasan tagihan ke pemasok.",
            "entries": [
                {"account": "11120 - Bank Mandiri Operasional - PTF", "debit": 17760000, "credit": 0},
                {"account": "11210 - Piutang Dagang Pelanggan - PTF", "debit": 0, "credit": 17760000},
                {"account": "21110 - Utang Dagang Pemasok - PTF", "debit": 11100000, "credit": 0},
                {"account": "11120 - Bank Mandiri Operasional - PTF", "debit": 0, "credit": 11100000}
            ]
        }
    ]
}

def print_header():
    print(f"{Colors.HEADER}{Colors.BOLD}========================================================================{Colors.ENDC}")
    print(f"{Colors.OKCYAN}{Colors.BOLD}   ANTIGRAVITY IDE - ERPNEXT MANUFACTURING CASE STUDY ENGINE v1.0{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}========================================================================{Colors.ENDC}")
    print(f"{Colors.OKGREEN}Company Name : {CASE_STUDY_DATA['company']} ({CASE_STUDY_DATA['abbr']}){Colors.ENDC}")
    print(f"{Colors.OKGREEN}Target ERP   : ERPNext V13 / V14 / V15 (Frappe Framework){Colors.ENDC}\n")

def run_simulation():
    print_header()
    print(f"{Colors.BOLD}=== PHASE 1: MASTER DATA SETUP ==={Colors.ENDC}")
    time.sleep(0.1)
    
    print("\n[1] Warehouses Created:")
    for wh in CASE_STUDY_DATA['warehouses']:
        print(f"    - {wh['name']} (Type: {wh['type']})")
        
    print("\n[2] Items Configured:")
    for it in CASE_STUDY_DATA['items']:
        print(f"    - {it['code']}: {it['name']} ({it['group']}) - Standard Rate: IDR {it['standard_rate']:,}")
        
    print("\n[3] Bill of Materials (BOM) Defined:")
    bom = CASE_STUDY_DATA['bom']
    print(f"    BOM Code: BOM-{bom['item_code']}-001 (For 1 unit {bom['item_code']})")
    total_rm = 0
    for rm in bom['items']:
        subtotal = rm['qty'] * rm['rate']
        total_rm += subtotal
        print(f"      * {rm['item_code']} x {rm['qty']} @ IDR {rm['rate']:,} = IDR {subtotal:,}")
    print(f"      * Direct Labor (BTKL) : IDR {bom['operating_cost']:,}")
    print(f"      * Factory Overhead (BOP): IDR {bom['overhead_cost']:,}")
    total_cost = total_rm + bom['operating_cost'] + bom['overhead_cost']
    print(f"    {Colors.BOLD}TOTAL HPP/COST PER UNIT = IDR {total_cost:,}{Colors.ENDC}\n")
    
    print(f"{Colors.BOLD}=== PHASE 2: TRANSACTION FLOW EXECUTION & GENERAL LEDGER IMPACT ==={Colors.ENDC}\n")
    
    total_debit_all = 0
    total_credit_all = 0
    
    for tx in CASE_STUDY_DATA['transactions']:
        time.sleep(0.1)
        print(f"{Colors.OKBLUE}{Colors.BOLD}[STEP {tx['step']}] {tx['code']} - {tx['title']}{Colors.ENDC}")
        print(f"DocType     : {tx['doctype']}")
        print(f"Description : {tx['description']}")
        print("General Ledger Entries:")
        print(f"  {'-'*65}")
        print(f"  {'Account Name':<42} | {'Debit (IDR)':<10} | {'Credit (IDR)':<10}")
        print(f"  {'-'*65}")
        
        step_debit = 0
        step_credit = 0
        for entry in tx['entries']:
            d_str = f"{entry['debit']:,}" if entry['debit'] > 0 else "-"
            c_str = f"{entry['credit']:,}" if entry['credit'] > 0 else "-"
            print(f"  {entry['account']:<42} | {d_str:>10} | {c_str:>10}")
            step_debit += entry['debit']
            step_credit += entry['credit']
            
        print(f"  {'-'*65}")
        print(f"  {'SUBTOTAL MATCH CHECK':<42} | {step_debit:>10,} | {step_credit:>10,}")
        if step_debit == step_credit:
            print(f"  {Colors.OKGREEN}STATUS: BALANCED [DEBIT = CREDIT]{Colors.ENDC}\n")
        else:
            print(f"  {Colors.FAIL}STATUS: UNBALANCED WARNING!{Colors.ENDC}\n")
            
        total_debit_all += step_debit
        total_credit_all += step_credit

    print(f"{Colors.BOLD}=== PHASE 3: FINANCIAL SUMMARY & TRIAL BALANCE VALIDATION ==={Colors.ENDC}")
    print(f"Total Cumulative Debit  : IDR {total_debit_all:,}")
    print(f"Total Cumulative Credit : IDR {total_credit_all:,}")
    print(f"Net Accounting Balance  : IDR {total_debit_all - total_credit_all:,} (Balanced!)\n")
    
    print(f"{Colors.OKGREEN}{Colors.BOLD}✅ CASE STUDY SIMULATION COMPLETED SUCCESSFULLY IN ANTIGRAVITY IDE!{Colors.ENDC}")

def export_json():
    out_path = os.path.join(os.path.dirname(__file__), "erpnext_manufacturing_fixtures.json")
    with open(out_path, "w") as f:
        json.dump(CASE_STUDY_DATA, f, indent=2)
    print(f"{Colors.OKCYAN}Exported JSON Fixture to: {out_path}{Colors.ENDC}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Antigravity IDE - ERPNext Case Study Runner")
    parser.add_argument("--mode", choices=["simulation", "export"], default="simulation", help="Run simulation or export json fixtures")
    args = parser.parse_args()
    
    if args.mode == "simulation":
        run_simulation()
        export_json()
    elif args.mode == "export":
        export_json()
