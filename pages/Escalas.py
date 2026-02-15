import streamlit as st
import pandas as pd

from utilidades import dia_semana, limpar_nome_arquivo
from dados import obter_dataframes
from preenchedores.escalas import gerar_docx_escalas

st.title("Escalas")

# 1️⃣Botão de atualização forçada
if st.button("🔄 Atualizar base de dados"):
    st.cache_data.clear()
    st.rerun()

# 2️⃣ Carregamento dos dados (cacheados)
dataframes = obter_dataframes()

# 3️⃣ Preparação dos dados
# Unindo as tabelas clientes e eventos
consolidado1 = pd.merge(
    dataframes["clientes"],
    dataframes["eventos"],
    on="ID_cliente",
    how="inner"
)

# 4️⃣ Criando a coluna "evento" (nome do evento no modelo 'nome - data')
consolidado1["evento"] = (
    consolidado1["NOME"].astype(str)
    + " - "
    + consolidado1["Data"].astype(str)
)
eventos = consolidado1[["ID_EVENTO", "evento", "Data", "Lugar"]]

# 5️⃣ Filtrando, do contas a pagar, somente os TIPO = 'Escala' e sem valor pago
escalas = dataframes["contas_a_pagar"].loc[(dataframes["contas_a_pagar"]["TIPO"] == "Escala") & (dataframes["contas_a_pagar"]["VALOR_PAGO"] == "")]
escalas = escalas[["ID_EVENTO", "ID_COLABORADOR", "VALOR"]]

# 6️⃣ Incluíndo informações dos eventos
escalas_com_eventos = pd.merge(
    escalas,
    eventos,
    on="ID_EVENTO",
    how="left"
)

# 7️⃣ Incluíndo as informações dos colaboradores
escalas_com_eventos_e_colaboradores = pd.merge(
    escalas_com_eventos,
    dataframes["colaboradores"],
    on="ID_COLABORADOR",
    how="left"
)

# 8️⃣ Unindo as tabelas clientes e eventos
consolidado2 = pd.merge(
    dataframes["clientes"],
    dataframes["eventos"],
    on="ID_cliente",
    how="inner"
)

# 9️⃣ Criando a coluna "evento" (nome do evento no modelo 'nome - data')
consolidado2["evento"] = (
    consolidado2["NOME"].astype(str)
    + " - "
    + consolidado2["Data"].astype(str)
)
eventos = consolidado2[["ID_EVENTO", "evento", "Data", "Lugar"]]

# 1️⃣0️⃣ Filtrando, do contas a pagar, somente os TIPO = 'Escala' e sem valor pago
todas_as_escalas = dataframes["contas_a_pagar"].loc[(dataframes["contas_a_pagar"]["TIPO"] == "Escala") & (dataframes["contas_a_pagar"]["VALOR_PAGO"] == "")]
todas_as_escalas = todas_as_escalas[["ID_EVENTO", "ID_COLABORADOR", "VALOR", "ID_CATEGORIA"]]

# 1️⃣1️⃣ Incluíndo informações dos eventos
escalas_com_eventos = pd.merge(
    todas_as_escalas,
    eventos,
    on="ID_EVENTO",
    how="left",
    suffixes=("", "_eventos")
)

# 1️⃣2️⃣ Incluíndo as informações dos colaboradores
escalas_com_eventos_e_colaboradores = pd.merge(
    escalas_com_eventos,
    dataframes["colaboradores"],
    on="ID_COLABORADOR",
    how="left",
    suffixes=("", "_colaboradores")
)

# 1️⃣3️⃣ Incluindo as informações da categoria
escalas_completas = pd.merge(
    escalas_com_eventos_e_colaboradores,
    dataframes["categorias"],
    on="ID_CATEGORIA",
    how="left",
    suffixes=('', '_categorias')
)

# 1️⃣4️⃣ Selecionando as colunas desejadas
escalas = escalas_completas[[
    'evento',
    "nome_colaborador",
    'Lugar',
    'VALOR',
    'CATEGORIA'
]]

print(escalas)

# 1️⃣5️⃣ Lista apenas eventos que possuem escalas
eventos_disponiveis = sorted(escalas["evento"].dropna().unique())

eventos_selecionados = st.multiselect(
    "Selecione um ou mais eventos para gerar as escalas",
    options=eventos_disponiveis
)

# 1️⃣6️⃣ Botão para gerar o arquivo
if eventos_selecionados:
    
    df_filtrado = escalas[
        escalas["evento"].isin(eventos_selecionados)
    ]

    if st.button("📄 Gerar arquivo de Escalas"):

        caminho = gerar_docx_escalas(df_filtrado)

        st.success("Arquivo gerado com sucesso!")

        with open(caminho, "rb") as file:
            st.download_button(
                label="📄 Baixar escalas.docx",
                data=file,
                file_name="escalas.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )