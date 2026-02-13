# dfs_iniciais.py atualizado para Streamlit Secrets
import gspread
import pandas as pd
import json
import streamlit as st
from oauth2client.service_account import ServiceAccountCredentials

def carregar_dataframes():
    # === CONFIGURAÇÕES INICIAIS ===
    escopo = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    # --- Credenciais do Streamlit Secrets ---
    # No secrets.toml, você deve ter:
    # [general]
    # GOOGLE_CREDENTIALS_JSON = """{ ...JSON do service account... }"""
    credenciais_dict = st.secrets["GOOGLE_CREDENTIALS_JSON"]
    credenciais = ServiceAccountCredentials.from_json_keyfile_dict(credenciais_dict, escopo)

    # --- Conexão com Google Sheets ---
    cliente = gspread.authorize(credenciais)
    planilha = cliente.open_by_key("1GXkH_2c_GTPUGlaFRQXDaKEH06o7RNnvoWOz5kw8jRE")

    # --- Abas que queremos carregar ---
    abas = ["EVENTOS", "CLIENTES", "RECEBIMENTOS", "COLABORADORES"]
    dataframes = {}

    for aba in abas:
        aba_escolhida = planilha.worksheet(aba)
        dados = aba_escolhida.get_all_values()
        if not dados:
            df = pd.DataFrame()  # caso a aba esteja vazia
        else:
            colunas = dados[0]
            registros = dados[1:]
            df = pd.DataFrame(registros, columns=colunas)
        dataframes[aba.lower()] = df
    
    return dataframes