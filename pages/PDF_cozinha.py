import streamlit as st
import pandas as pd

from utilidades import dia_semana, limpar_nome_arquivo
from dados import obter_dataframes   # ✅ padrão correto
from preenchedor import preencher_modelo

st.title("Gerar PDF para a cozinha")

# ------------------------------------
# Botão de atualização forçada
# ------------------------------------
if st.button("🔄 Atualizar base de dados"):
    st.cache_data.clear()
    st.rerun()

# ------------------------------------
# Carregamento dos dados (cacheados)
# ------------------------------------
dataframes = obter_dataframes()

# ------------------------------------
# Preparação dos dados
# ------------------------------------
consolidado = pd.merge(
    dataframes["clientes"],
    dataframes["eventos"],
    on="ID_cliente",
    how="inner"
)

consolidado["evento"] = (
    consolidado["NOME"].astype(str)
    + " - "
    + consolidado["Data"].astype(str)
)

# ------------------------------------
# Interface
# ------------------------------------
evento_selecionado = st.selectbox(
    "Selecione o evento",
    options=consolidado["evento"].tolist()
)

linha_df = consolidado.loc[consolidado["evento"] == evento_selecionado]

if linha_df.empty:
    st.error("Evento não encontrado.")
    st.stop()

linha = linha_df.iloc[0]

# ------------------------------------
# Dados para o template
# ------------------------------------
dados = {
    "nome": linha["NOME"],
    "ocasiao": linha["ocasiao"],
    "data": linha["Data"],
    "hora": linha["Hora"].replace(":00", ""),
    "convidados": linha["Convidados"],
    "staffs": linha["staff"],
    "endereco": linha["Lugar"],
    "tipo": linha["Tipo"],
    "observacao": linha["Nota"],
    "menu": linha["Menu"],
    "dia": dia_semana(linha["Data"]),
}

modelo = st.radio(
    "Escolha o modelo",
    ["Com observações", "Sem observações"],
    index=None
)

# ------------------------------------
# Geração do documento
# ------------------------------------
if modelo:
    nome_cliente_limpo = limpar_nome_arquivo(dados["nome"])

    documento_path = preencher_modelo(
        dados=dados,
        nome_modelo=f"{modelo}.docx",
        nome_saida=f"{nome_cliente_limpo} - {modelo}.docx"
    )

    with open(documento_path, "rb") as file:
        st.download_button(
            label="Baixar documento",
            data=file,
            file_name=documento_path.name,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
