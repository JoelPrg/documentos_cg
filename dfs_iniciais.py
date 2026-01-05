import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

def carregar_dataframes():
    # === CONFIGURAÇÕES INICIAIS ===
    escopo = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credenciais = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", escopo)
    cliente = gspread.authorize(credenciais)
    planilha = cliente.open_by_key("1GXkH_2c_GTPUGlaFRQXDaKEH06o7RNnvoWOz5kw8jRE")

    abas = ["EVENTOS", "CLIENTES", "RECEBIMENTOS"]
    dataframes = {}

    for aba in abas:
        aba_escolhida = planilha.worksheet(aba)
        dados = aba_escolhida.get_all_values()
        colunas = dados[0]
        registros = dados[1:]
        df = pd.DataFrame(registros, columns=colunas)
        dataframes[aba.lower()] = df
    
    return dataframes

dataframes = carregar_dataframes()