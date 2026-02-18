import streamlit as st
import pandas as pd
from datetime import timedelta, date
from utilidades import formato_br_data

from dados import obter_dataframes
from preenchedores.preencher_contas_a_pagar import gerar_contas_a_pagar

st.title("Contas a pagar")

# 1️⃣ Botão de atualização forçada
if st.button("🔄 Atualizar base de dados"):
    st.cache_data.clear()
    st.rerun()

# 2️⃣ Carregamento dos dados (cacheados)
dataframes = obter_dataframes()

# 3️⃣ Data inicial
data_inicial = st.date_input("Data inicial", value=None)

if data_inicial is None:
    st.warning("Selecione a data inicial para continuar.")
    st.stop()

# 4️⃣ Lógica de data final conforme dia da semana
# weekday(): 0=seg, 1=ter, 2=qua, 3=qui, 4=sex, 5=sab, 6=dom

if data_inicial.weekday() == 5:  # Sábado
    # Opções: próxima sexta (6 dias à frente) ou o próprio sábado (mesmo dia)
    opcoes_data_final = {
        f"Somente sábado ({data_inicial.strftime('%d/%m/%Y')})": data_inicial,
        f"Semana completa até sexta ({(data_inicial + timedelta(days=6)).strftime('%d/%m/%Y')})": data_inicial + timedelta(days=6),
    }

    escolha = st.radio(
        "A data inicial é um sábado. Selecione o período:",
        options=list(opcoes_data_final.keys()),
        index=1  # padrão: semana completa
    )

    data_final = opcoes_data_final[escolha]

else:
    # Não é sábado: data final = data inicial (dia único)
    data_final = data_inicial
    st.info(f"Como a data inicial não é sábado, o relatório será gerado somente para o dia {data_inicial.strftime('%d/%m/%Y')}.")

st.success(f"Período selecionado: {data_inicial.strftime('%d/%m/%Y')} até {data_final.strftime('%d/%m/%Y')}")

# 5️⃣ Preparando dataframe
df = dataframes["contas_a_pagar"].copy()

# Garantir que vencimento é datetime (sem horário para o filtro funcionar corretamente)
df["VENCIMENTO"] = pd.to_datetime(df["VENCIMENTO"], dayfirst=True, errors="coerce").dt.normalize()

# 6️⃣ Aplicando filtro
contas = df.loc[
    (df["TIPO"] != "Escala") &
    (df["VALOR_PAGO"].isna() | (df["VALOR_PAGO"] == "")) &
    (df["VENCIMENTO"] >= pd.to_datetime(data_inicial)) &
    (df["VENCIMENTO"] <= pd.to_datetime(data_final))
].sort_values("VENCIMENTO")

# 7️⃣ Deixando apenas as colunas necessárias
contas = contas[["VENCIMENTO", "VALOR", "DESCRICAO"]]

# 8️⃣ Feedback visual
if contas.empty:
    st.warning("Nenhuma conta encontrada para o período selecionado.")
else:
    agrupado = (
        contas
        .groupby(contas["VENCIMENTO"].dt.date)
        .size()
        .reset_index(name="Quantidade")
    )
    agrupado.columns = ["Data", "Quantidade"]
    agrupado["Data"] = agrupado["Data"].apply(lambda d: d.strftime("%d/%m/%Y"))
    #st.dataframe(agrupado, use_container_width=True, hide_index=True)

# 9️⃣ Gerar e baixar DOCX
if not contas.empty:
    if st.button("📄 Gerar DOCX"):
        caminho_docx = gerar_contas_a_pagar(contas)
        if caminho_docx:
            st.session_state["caminho_docx"] = caminho_docx
        else:
            st.error("Erro ao gerar o documento.")

    if "caminho_docx" in st.session_state:
        with open(st.session_state["caminho_docx"], "rb") as f:
            st.download_button(
                "⬇️ Baixar DOCX",
                f,
                file_name="contas.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )