import streamlit as st
import pandas as pd

# Configuração da página (UI/UX)
st.set_page_config(
    page_title="GeminiFruti - Auditoria SAP",
    page_icon="🍇",
    layout="wide"
)

# Estilização do cabeçalho
st.title("🍇 GeminiFruti LTDA")
st.subheader("Painel Executivo de Auditoria de Recebimento (SAP / MIGO)")
st.markdown("---")

# Função para carregar os dados
@st.cache_data
def carregar_dados():
    df = pd.read_csv("dados_sap.csv")
    df['divergencia'] = df['qty_pedido'] - df['qty_recebido']
    
    # Cálculo do Lead Time
    df['data_emissao'] = pd.to_datetime(df['data_emissao'])
    df['data_recebimento'] = pd.to_datetime(df['data_recebimento'])
    df['lead_time'] = (df['data_recebimento'] - df['data_emissao']).dt.days
    
    # Status visual
    df['status'] = df['divergencia'].apply(
        lambda x: f"⚠️ Faltam {x} un/cx" if x > 0 else "✅ OK"
    )
    return df

df = carregar_dados()

# --- 📊 SEÇÃO DE KPIS (CARDS EXECUTIVOS) ---
total_pedidos = len(df)
pedidos_divergentes = len(df[df['divergencia'] > 0])
total_faltante = df['divergencia'].sum()
lead_time_medio = round(df['lead_time'].mean(), 1)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Total de Pedidos Auditados", value=total_pedidos)

with col2:
    st.metric(
        label="Pedidos com Divergência", 
        value=pedidos_divergentes, 
        delta=f"{(pedidos_divergentes/total_pedidos)*100:.0f}% do total", 
        delta_color="inverse"
    )

with col3:
    st.metric(label="Volume Faltante (Unidades)", value=total_faltante, delta=f"-{total_faltante}", delta_color="inverse")

with col4:
    st.metric(label="Lead Time Médio", value=f"{lead_time_medio} dias")

st.markdown("---")

# --- 🔍 FILTROS INTERATIVOS ---
st.sidebar.header("🔍 Filtros da Auditoria")
status_filtro = st.sidebar.radio(
    "Exibir Pedidos:",
    ["Todos", "Apenas Divergências", "Apenas OK"]
)

df_filtrado = df.copy()
if status_filtro == "Apenas Divergências":
    df_filtrado = df[df['divergencia'] > 0]
elif status_filtro == "Apenas OK":
    df_filtrado = df[df['divergencia'] == 0]

# --- 📋 TABELA INTERATIVA ---
st.write("### 📜 Detalhamento das Ordens de Compra (PO)")

st.dataframe(
    df_filtrado[[
        "po_number", "sku", "descricao", "qty_pedido", 
        "qty_recebido", "divergencia", "lead_time", "status"
    ]],
    column_config={
        "po_number": "Ordem (PO)",
        "sku": "Código SKU",
        "descricao": "Produto / Hortifrúti",
        "qty_pedido": "Qtd. Pedida",
        "qty_recebido": "Qtd. Recebida",
        "divergencia": "Divergência",
        "lead_time": "Lead Time (Dias)",
        "status": "Status do Recebimento"
    },
    use_container_width=True,
    hide_index=True
)