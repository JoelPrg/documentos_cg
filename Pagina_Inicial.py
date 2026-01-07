import streamlit as st
from dfs_iniciais import carregar_dataframes

st.set_page_config(page_title="Página Inicial")
st.title("Página Inicial")

# -------------------------------
# Cache SEM TTL (só atualiza quando limpar)
# -------------------------------
@st.cache_data
def obter_dataframes():
    return carregar_dataframes()

# Botão de atualização forçada
if st.button("🔄 Atualizar base de dados"):
    st.cache_data.clear()
    st.experimental_rerun()

# Carregamento normal
dataframes = obter_dataframes()

# Exemplo de uso
st.subheader("Eventos")
st.dataframe(dataframes["eventos"])
