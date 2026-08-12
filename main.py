import csv
from datetime import datetime

def carregar_dados_sap(caminho_arquivo):
    pedidos = []
    with open(caminho_arquivo, mode='r', encoding='utf-8') as file:
        leitor = csv.DictReader(file)
        for linha in leitor:
            pedidos.append({
                "po_number": linha["po_number"],
                "sku": linha["sku"],
                "descricao": linha["descricao"],
                "qty_pedido": int(linha["qty_pedido"]),
                "qty_recebido": int(linha["qty_recebido"]),
                "data_emissao": linha["data_emissao"],
                "data_recebimento": linha["data_recebimento"]
            })
    return pedidos

def auditar_recebimento_geminifruti(pedidos):
    print("\n" + "=" * 70)
    print(" 🍇 GEMINIFRUTI LTDA - RELATÓRIO DE AUDITORIA DE RECEBIMENTO (SAP / MIGO)")
    print("=" * 70)
    
    total_faltante = 0
    total_pedidos = len(pedidos)
    pedidos_com_divergencia = 0

    for item in pedidos:
        diff = item["qty_pedido"] - item["qty_recebido"]
        
        # Cálculo simples de Lead Time em dias
        d_emissao = datetime.strptime(item["data_emissao"], "%Y-%m-%d")
        d_receb = datetime.strptime(item["data_recebimento"], "%Y-%m-%d")
        lead_time = (d_receb - d_emissao).days

        if diff > 0:
            status = f"⚠️ DIVERGÊNCIA: Faltam {diff} un/cx"
            total_faltante += diff
            pedidos_com_divergencia += 1
        else:
            status = "✅ OK (Recebimento Total)"

        print(f"PO: {item['po_number']} | SKU: {item['sku']:<8} | {item['descricao']:<23} | Lead Time: {lead_time}d | {status}")

    print("-" * 70)
    print(f"📊 RESUMO EXECUTIVO:")
    print(f"   • Total de Pedidos Auditados: {total_pedidos}")
    print(f"   • Pedidos com Divergência:   {pedidos_com_divergencia}")
    print(f"   • Volume Total Retido/Faltante: {total_faltante} unidades")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    dados = carregar_dados_sap("dados_sap.csv")
    auditar_recebimento_geminifruti(dados)