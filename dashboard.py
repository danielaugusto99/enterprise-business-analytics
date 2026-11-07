import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Configuração da Página
st.set_page_config(
    page_title="Enterprise Business Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Enterprise Business Analytics Dashboard")
st.markdown("Painel interativo de alta performance para monitoramento de vendas, KPIs estratégicos e análise temporal.")

# 1. Geração de Dados Sintéticos Realistas (Mock Data)
@st.cache_data
def load_data():
    np.random.seed(42)
    dates = pd.date_range(start="2025-01-01", end="2026-06-01", freq="D")
    df = pd.DataFrame({
        'date': np.random.choice(dates, 1500),
        'region': np.random.choice(['Nordeste', 'Sudeste', 'Sul', 'Centro-Oeste', 'Norte'], 1500),
        'category': np.random.choice(['Tecnologia', 'Móveis', 'Suprimentos', 'Serviços'], 1500),
        'sales': np.random.uniform(150, 6000, 1500),
        'units': np.random.randint(1, 25, 1500)
    })
    df['profit'] = df['sales'] * np.random.uniform(0.15, 0.45, 1500)
    return df

df = load_data()

# 2. Sidebar - Filtros Dinâmicos
st.sidebar.header("Filtros Globais")
selected_region = st.sidebar.multiselect(
    "Selecione a Região:",
    options=df['region'].unique(),
    default=df['region'].unique()
)

selected_category = st.sidebar.multiselect(
    "Selecione a Categoria:",
    options=df['category'].unique(),
    default=df['category'].unique()
)

# Filtragem do DataFrame
filtered_df = df[
    (df['region'].isin(selected_region)) & 
    (df['category'].isin(selected_category))
]

# 3. Métricas Principais (KPI Cards)
total_sales = filtered_df['sales'].sum()
total_profit = filtered_df['profit'].sum()
total_units = filtered_df['units'].sum()
avg_ticket = total_sales / len(filtered_df) if len(filtered_df) > 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Vendas Totais", f"R$ {total_sales:,.2f}")
col2.metric("Lucro Líquido", f"R$ {total_profit:,.2f}")
col3.metric("Unidades Vendidas", f"{total_units:,}")
col4.metric("Ticket Médio", f"R$ {avg_ticket:,.2f}")

st.markdown("---")

# 4. Gráficos Interativos com Plotly
c1, c2 = st.columns(2)

with c1:
    st.subheader("Desempenho de Vendas por Categoria")
    cat_sales = filtered_df.groupby('category')['sales'].sum().reset_index()
    fig_cat = px.bar(cat_sales, x='category', y='sales', color='category', text_auto='.2s', template='plotly_dark')
    st.plotly_chart(fig_cat, use_container_width=True)

with c2:
    st.subheader("Evolução Temporal das Vendas (Semanal)")
    time_sales = filtered_df.groupby(pd.Grouper(key='date', freq='W'))['sales'].sum().reset_index()
    fig_time = px.line(time_sales, x='date', y='sales', markers=True, template='plotly_dark')
    st.plotly_chart(fig_time, use_container_width=True)

# Tabela Detalhada de Dados Filtrados
with st.expander("🔍 Visualizar Dados Brutos Filtrados"):
    st.dataframe(filtered_df, use_container_width=True)