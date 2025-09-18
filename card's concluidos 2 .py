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
tabela_mensal['Atingimento (%)'] = ((tabela_mensal['Realizado']/tabela_mensal['Meta'])*100)
tabela_mensal['Atingimento (%)'] = tabela_mensal['Atingimento (%)'].apply(lambda x: f"{x:.2f}%")

st.dataframe(
    tabela_mensal.style.applymap(
        lambda val: 'background-color: #d4edda;' if float(str(val).replace('%',''))>=100 else 'background-color: #f8d7da;',
        subset=['Atingimento (%)']
    )
)

# --- GRÁFICOS MENSAL ---
if not tabela_mensal.empty:
    # Pizza
    total_realizado = tabela_mensal['Realizado'].sum()
    total_meta = tabela_mensal['Meta'].sum()
    fig_mensal_pie = px.pie(
        names=['Atingido','Não atingido'],
        values=[total_realizado, max(0,total_meta-total_realizado)],
        color=['Atingido','Não atingido'],
        color_discrete_map={'Atingido':'#28a745','Não atingido':'#dc3545'},
        title="Meta Mensal"
    )
    st.plotly_chart(fig_mensal_pie)

# --- TABELA ANUAL (2º Semestre) ---
st.header("📊 Consolidado Anual (Julho a Dezembro)")
meses_2_semestre_default = ["Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"]
meses_2_semestre = st.sidebar.multiselect("Meses (2º Semestre)", meses_2_semestre_default, default=meses_2_semestre_default)
df_2_semestre = df[(df['Ano']==ano_selecionado) & (df['Mês'].isin(meses_2_semestre))]
tabela_anual = df_2_semestre.groupby('Comercial_Padronizado').size().reset_index(name='Realizado')
tabela_anual['Meta'] = tabela_anual['Comercial_Padronizado'].apply(lambda x: meta_mensal_total(x, meses_2_semestre))
tabela_anual['Atingimento (%)'] = ((tabela_anual['Realizado']/tabela_anual['Meta'])*100)
tabela_anual['Atingimento (%)'] = tabela_anual['Atingimento (%)'].apply(lambda x: f"{x:.2f}%")

st.dataframe(
    tabela_anual.style.applymap(
        lambda val: 'background-color: #d4edda;' if float(str(val).replace('%',''))>=100 else 'background-color: #f8d7da;',
        subset=['Atingimento (%)']
    )
)
