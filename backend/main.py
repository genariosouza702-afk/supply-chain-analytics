"""
Supply Chain Analytics Module
Módulo para análise de desempenho de pedidos e divergências de estoque/recebimento.
"""

# Dados simulados de Ordens de Compra e Recebimentos Físicos
purchase_orders = [
    {"po_number": "45000101", "sku": "MAT-8841", "qty_ordered": 500, "qty_received": 500, "lead_time_days": 4},
    {"po_number": "45000102", "sku": "MAT-9920", "qty_ordered": 1200, "qty_received": 1150, "lead_time_days": 12},
    {"po_number": "45000103", "sku": "MAT-1102", "qty_ordered": 300, "qty_received": 300, "lead_time_days": 5},
    {"po_number": "45000104", "sku": "MAT-8841", "qty_ordered": 800, "qty_received": 750, "lead_time_days": 9},
]

def analyze_po_discrepancies(orders):
    print("=" * 60)
    print(" 📦 AUDITORIA DE RECEBIMENTO E PERFORMANCE DE FORNECEDORES")
    print("=" * 60)
    
    total_discrepancy = 0

    for item in orders:
        diff = item["qty_ordered"] - item["qty_received"]
        total_discrepancy += diff
        
        status = "✅ OK" if diff == 0 else f"⚠️ DIVERGÊNCIA ({diff} un faltantes)"
        
        print(f"PO: {item['po_number']} | SKU: {item['sku']} | Lead Time: {item['lead_time_days']} dias | Status: {status}")
        
    print("-" * 60)
    print(f"Total acumulado de divergências no recebimento: {total_discrepancy} unidades.")
    print("=" * 60)

if __name__ == "__main__":
    analyze_po_discrepancies(purchase_orders)