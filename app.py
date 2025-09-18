
import streamlit as st
import pandas as pd
import plotly.express as px

# --- CONFIGURAÇÕES ---
st.set_page_config(page_title="Dashboard de Metas", layout="wide", page_icon="📊")

URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSlQ9u5x09qR0dAKJsMC-fXTvJWRWPzMrXpaGaojOPblRrJYbx4Q-xalzh2hmf2WtwHRoLVIBOdL_HC/pub?output=csv"

# --- MAPEAMENTOS ---
NOME_MAPPING = {
    'Werbet': 'Werbet', 'Werker Alencar': 'Werbet', 'Werbet Alencar': 'Werbet',
    'Pamela': 'Pamela', 'Pamela Crédita': 'Pamela', 'Pamela Cri': 'Pamela', 'Pamela Cristina': 'Pamela',
    'Ana Clara': 'Ana Clara', 'Ana Clara Souza': 'Ana Clara',
    'Danilo': 'Danilo', 'Danilo Neder': 'Danilo',
    'Natalie': 'Natalie', 'Natalie Lopes': 'Natalie',
    'Andressa': 'Andressa',
    'Rafael': 'Rafael', 'Rafael Miguel': 'Rafael',
    'Thaís': 'Thaís', 'Thais Mendonca': 'Thaís', 'Thais': 'Thaís', 'Thaki': 'Thaís'
}

# META MENSAL POR COMERCIAL
META_MENSAL_POR_COMERCIAL = {
    "Janeiro": { "Andressa": 22, "Rafael": 22, "Thaís": 22, "Ana Clara": 44, "Danilo": 44, "Pamela": 44, "Natalie": 44, "Werbet": 44 },
    "Fevereiro": { "Andressa": 20, "Rafael": 20, "Thaís": 20, "Ana Clara": 40, "Danilo": 40, "Pamela": 40, "Natalie": 40, "Werbet": 40 },
    "Março": { "Andressa": 21, "Rafael": 21, "Thaís": 21, "Ana Clara": 42, "Danilo": 42, "Pamela": 42, "Natalie": 42, "Werbet": 42 },
    "Abril": { "Andressa": 22, "Rafael": 22, "Thaís": 22, "Ana Clara": 44, "Danilo": 44, "Pamela": 44, "Natalie": 44, "Werbet": 44 },
    "Maio": { "Andressa": 22, "Rafael": 22, "Thaís": 22, "Ana Clara": 44, "Danilo": 44, "Pamela": 44, "Natalie": 44, "Werbet": 44 },
    "Junho": { "Andressa": 21, "Rafael": 21, "Thaís": 21, "Ana Clara": 42, "Danilo": 42, "Pamela": 42, "Natalie": 42, "Werbet": 42 },
    "Julho": { "Andressa": 23, "Rafael": 23, "Thaís": 23, "Ana Clara": 46, "Danilo": 46, "Pamela": 46, "Natalie": 46, "Werbet": 46 },
    "Agosto": { "Andressa": 21, "Rafael": 21, "Thaís": 21, "Ana Clara": 42, "Danilo": 42, "Pamela": 42, "Natalie": 42, "Werbet": 42 },
    "Setembro": { "Andressa": 22, "Rafael": 22, "Thaís": 22, "Ana Clara": 44, "Danilo": 44, "Pamela": 44, "Natalie": 44, "Werbet": 44 },
    "Outubro": { "Andressa": 23, "Rafael": 23, "Thaís": 23, "Ana Clara": 46, "Danilo": 46, "Pamela": 46, "Natalie": 46, "Werbet": 46 },
    "Novembro": { "Andressa": 21, "Rafael": 21, "Thaís": 21, "Ana Clara": 42, "Danilo": 42, "Pamela": 42, "Natalie": 42, "Werbet": 42 },
    "Dezembro": { "Andressa": 22, "Rafael": 22, "Thaís": 22, "Ana Clara": 44, "Danilo": 44, "Pamela": 44, "Natalie": 44, "Werbet": 44 }
}

# --- FUNÇÃO PARA CALCULAR META ---
def meta_mensal_total(nome, meses):
    return sum(META_MENSAL_POR_COMERCIAL[m].get(nome, 0) for m in meses)

# --- CARREGAR DADOS ---
@st.cache_data
def load_data():
    df = pd.read_csv(URL)
    df['Data de Conclusão'] = pd.to_datetime(df['Data de Conclusão'], dayfirst=True, errors='coerce')
    df.dropna(subset=['Data de Conclusão'], inplace=True)
    df['Ano'] = df['Data de Conclusão'].dt.year
    df['Mês'] = df['Data de Conclusão'].dt.strftime('%B')
    meses_trad = {
        'January': 'Janeiro', 'February': 'Fevereiro', 'March': 'Março', 'April': 'Abril',
        'May': 'Maio', 'June': 'Junho', 'July': 'Julho', 'August': 'Agosto', 'September': 'Setembro',
        'October': 'Outubro', 'November': 'Novembro', 'December': 'Dezembro'
    }
    df['Mês'] = df['Mês'].map(meses_trad).fillna(df['Mês'])
    df['Comercial_Padronizado'] = df['Comercial/Capitão']
    for nome_ori, nome_pad in NOME_MAPPING.items():
        df.loc[df['Comercial/Capitão'].str.contains(nome_ori, case=False, na=False), 'Comercial_Padronizado'] = nome_pad
    return df

df = load_data()

# --- FILTROS ---
st.sidebar.header("Filtros")
anos_disponiveis = df['Ano'].sort_values().unique()
ano_selecionado = st.sidebar.selectbox("Ano", anos_disponiveis, index=len(anos_disponiveis)-1)
meses_disponiveis = df['Mês'].unique()
meses_selecionados = st.sidebar.multiselect("Meses (Mensal)", meses_disponiveis, default=meses_disponiveis)

# --- TABELA MENSAL ---
st.header("📊 Tabela de Performance Mensal")
df_filtrado = df[(df['Ano']==ano_selecionado) & (df['Mês'].isin(meses_selecionados))]
tabela_mensal = df_filtrado.groupby('Comercial_Padronizado').size().reset_index(name='Realizado')
tabela_mensal['Meta'] = tabela_mensal['Comercial_Padronizado'].apply(lambda x: meta_mensal_total(x, meses_selecionados))
tabela_mensal['Atingimento (%)'] = ((tabela_mensal['Realizado']/tabela_mensal['Meta'])*100).round(2)
tabela_mensal['Atingimento (%)'] = tabela_mensal['Atingimento (%)'].astype(str) + '%'

# Estilo de cores
st.dataframe(
    tabela_mensal.style.applymap(
        lambda val: 'background-color: #d4edda;' if float(str(val).replace('%',''))>=100 else 'background-color: #f8d7da;',
        subset=['Atingimento (%)']
    )
)

# --- GRÁFICOS MENSAL ---
if not tabela_mensal.empty:
    tabela_mensal['Cor'] = tabela_mensal['Atingimento (%)'].apply(lambda x: '#28a745' if float(x.replace('%',''))>=100 else '#dc3545')
    fig_mensal_bar = px.bar(
        tabela_mensal,
        x='Comercial_Padronizado',
        y='Atingimento (%)',
        color='Cor',
        color_discrete_map='identity',
        text='Atingimento (%)',
        title='Atingimento por Comercial (Mensal)'
    )
    fig_mensal_bar.update_layout(yaxis=dict(range=[0, max(120, tabela_mensal['Atingimento (%)'].apply(lambda x: float(x.replace('%',''))).max()+10)]))
    st.plotly_chart(fig_mensal_bar)
