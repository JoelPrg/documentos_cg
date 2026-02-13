import streamlit as st
import pandas as pd

from utilidades import dia_semana, limpar_nome_arquivo
from dados import obter_dataframes
from preenchedor import preencher_modelo

st.title("Gerar PDF de escalas")

# Botão de atualização forçada
if st.button("🔄 Atualizar base de dados"):
    st.cache_data.clear()
    st.rerun()

# Carregamento dos dados (cacheados)
dataframes = obter_dataframes()

# Preparação dos dados
# Mesclagem de clientes e eventos
consolidado1 = pd.merge(
    dataframes["clientes"],
    dataframes["eventos"],
    on="ID_cliente",
    how="inner"
)

consolidado1["evento"] = (
    consolidado1["NOME"].astype(str)
    + " - "
    + consolidado1["Data"].astype(str)
)

# Mesclagem de escalas e colaboradores
consolidado2 = pd.merge(
    dataframes["escalas"],
    dataframes["colaboradores"],
    on="ID_colaborador",
    how="inner"
)

# Mesclagem final
consolidado = pd.merge(
    consolidado1,
    consolidado2,
    on="ID_evento",
    how="left"
)

# Interface
evento_selecionado = st.selectbox(
    "Selecione o evento",
    options=consolidado["evento"].tolist()
)

linha_df = consolidado.loc[consolidado["evento"] == evento_selecionado]
if linha_df.empty:
    st.error("Evento não encontrado.")
    st.stop()

linha = linha_df.iloc[0]

# Dados para o template
dados = {
    "nome": linha["NOME"],
    "data": linha["Data"],
    "hora": linha["Hora"].replace(":00", ""),
    "convidados": linha["Convidados"],
    "endereco": linha["Lugar"],
    "dia": dia_semana(linha["Data"]),
}

valores_padrao = {
    "Garçom": "R$ 180,00",
    "Auxiliar de Cozinha": "R$ 150,00",
    "Copeiro": "R$ 150,00",
    "Banheirista": "R$ 120,00"
}

# script para gerar a lista de dicionários dos colaboradores da escala do evento selecionado
colaboradores_evento = consolidado2.loc[consolidado2["ID_evento"] == linha["ID_evento"]]
lista_colaboradores = []
for _, colab in colaboradores_evento.iterrows():
    colaborador_info = {
        "nome_colaborador": colab["Nome_colaborador"],
        "funcao": colab["Função"],
        "horario": valores_padrao[colab["Função"]],
    }
    lista_colaboradores.append(colaborador_info)


# Geração do documento
nome_cliente_limpo = limpar_nome_arquivo(dados["nome"])

documento_path = preencher_modelo(
    dados=dados,
    nome_modelo="escala.docx",
    nome_saida=f"{nome_cliente_limpo} - escala.docx"
)

with open(documento_path, "rb") as file:
    st.download_button(
        label="Baixar documento",
        data=file,
        file_name=documento_path.name,
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
