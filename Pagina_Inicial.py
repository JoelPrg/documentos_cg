import streamlit as st
from dfs_iniciais import carregar_dataframes

st.set_page_config(page_title="Página Inicial")
st.title("Página Inicial")
st.text("Local temporário para geração de documentos do CG")
st.text("Em desenvolvimento...")

# Cache SEM TTL (só atualiza quando limpar)
@st.cache_data
def obter_dataframes():
    return carregar_dataframes()

# Carregamento normal
dataframes = obter_dataframes()