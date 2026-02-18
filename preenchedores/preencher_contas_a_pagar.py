import pandas as pd
from docxtpl import DocxTemplate
from utilidades import formato_br_data


def gerar_contas_a_pagar(recebimentos,
                         caminho_modelo="modelos/Contas.docx",
                         caminho_saida="recebimentos.docx"):

    if recebimentos.empty:
        return None

    recebimentos = recebimentos.copy()
    recebimentos["VENCIMENTO"] = pd.to_datetime(recebimentos["VENCIMENTO"], dayfirst=True, errors="coerce").dt.normalize()
    recebimentos = recebimentos.sort_values("VENCIMENTO")

    # 🔹 Normalizar valores para float
    recebimentos["VALOR"] = (
        recebimentos["VALOR"]
        .astype(str)
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
        .astype(float)
    )

    # =====================================================
    # 1️⃣ Montar lista de dias com itens
    # =====================================================

    dias_lista = []

    for dia, df_dia in recebimentos.groupby(recebimentos["VENCIMENTO"].dt.date):

        itens = []
        total = df_dia["VALOR"].sum()

        for _, row in df_dia.iterrows():
            itens.append({
                "descricao": row["DESCRICAO"],
                "valor": f"R$ {row['VALOR']:,.2f}"
            })

        dias_lista.append({
            "data": dia,
            "weekday": dia.weekday(),  # 0=seg ... 5=sab, 6=dom
            "itens": itens,
            "total": f"R$ {total:,.2f}"
        })

    # Ordenar por data
    dias_lista.sort(key=lambda x: x["data"])

    # =====================================================
    # 2️⃣ Agrupar sábado/domingo/segunda em um único bloco
    #    Apenas os que existirem no dataframe serão incluídos
    # =====================================================

    blocos = []
    datas_usadas = set()

    # Verificar se o período começa num sábado
    primeiro_dia = dias_lista[0] if dias_lista else None
    periodo_comeca_sabado = primeiro_dia and primeiro_dia["weekday"] == 5

    if periodo_comeca_sabado:
        # Coletar sábado, domingo e segunda que existam na lista
        dias_fim_semana = [d for d in dias_lista if d["weekday"] in (5, 6, 0)]
        dias_semana_normal = [d for d in dias_lista if d["weekday"] not in (5, 6, 0)]

        # Bloco sáb/dom/seg (apenas os que tiverem dados)
        if dias_fim_semana:
            blocos.append({"dias": dias_fim_semana})
            for d in dias_fim_semana:
                datas_usadas.add(d["data"])

        # Demais dias: cada um em seu próprio bloco
        for dia in dias_semana_normal:
            if dia["data"] not in datas_usadas:
                blocos.append({"dias": [dia]})
                datas_usadas.add(dia["data"])
    else:
        # Período começa em dia comum: cada dia é um bloco individual
        for dia in dias_lista:
            blocos.append({"dias": [dia]})

    # =====================================================
    # 3️⃣ Controle de quebra de página
    # =====================================================

    for idx, bloco in enumerate(blocos):
        bloco["quebra_pagina"] = (idx < len(blocos) - 1)

    # =====================================================
    # 4️⃣ Renderizar
    # =====================================================

    doc = DocxTemplate(caminho_modelo)

    contexto = {
        "blocos": blocos,
        "formato_br_data": formato_br_data
    }

    doc.render(contexto)
    doc.save(caminho_saida)

    return caminho_saida