import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Senadores - Contatos Institucionais", layout="wide")
st.title("🏛️ Painel Interativo - Senadores do Brasil")
st.markdown("Consulte informações de contato e dados institucionais dos senadores em exercício.")

# 🛠️ Etapa de diagnóstico e carregamento seguro do CSV
try:
    df = pd.read_csv("Contato Senadores.csv", encoding="latin1", sep=";", engine="python")
    df.columns = df.columns.str.strip().str.upper()
    st.success("✅ CSV carregado com sucesso!")
    st.write("📋 Colunas detectadas no arquivo:", df.columns.tolist())
except Exception as e:
    st.error(f"❌ Erro ao carregar o CSV: {e}")
    st.stop()

# Filtros interativos
col1, col2, col3 = st.columns(3)
with col1:
    partido = st.selectbox("Filtrar por Partido", ["Todos"] + sorted(df["PARTIDO"].dropna().unique()))
with col2:
    uf = st.selectbox("Filtrar por UF", ["Todos"] + sorted(df["UF"].dropna().unique()))
with col3:
    titularidade = st.selectbox("Filtrar por Titularidade", ["Todos"] + sorted(df["TITULARIDADE"].dropna().unique()))

# Aplicar filtros
filtro = df.copy()
if partido != "Todos":
    filtro = filtro[filtro["PARTIDO"] == partido]
if uf != "Todos":
    filtro = filtro[filtro["UF"] == uf]
if titularidade != "Todos":
    filtro = filtro[filtro["TITULARIDADE"] == titularidade]

# Campo de busca por nome
busca = st.text_input("🔍 Buscar por nome do senador")
if busca:
    filtro = filtro[filtro["NOME_PARLAMENTAR"].str.contains(busca, case=False)]

# Tabela final
st.markdown(f"### 📋 Lista de Senadores ({len(filtro)} encontrados)")
st.dataframe(
    filtro[[
        "NOME_PARLAMENTAR", "PARTIDO", "UF", "TITULARIDADE", "MANDATO",
        "TELEFONES", "DTNASC", "EMAIL", "CHEFE_GAB"
    ]].reset_index(drop=True),
    use_container_width=True
)
