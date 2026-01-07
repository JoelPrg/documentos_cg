import streamlit as st
from dfs_iniciais import carregar_dataframes

@st.cache_data
def obter_dataframes():
    return carregar_dataframes()
