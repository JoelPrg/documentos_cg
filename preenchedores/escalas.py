from pathlib import Path
from docxtpl import DocxTemplate


def gerar_docx_escalas(df):
    """
    Gera um único arquivo 'escalas.docx'
    contendo todos os lugares/eventos selecionados.
    """

    base_path = Path(__file__).resolve().parent.parent
    modelo_path = base_path / "modelos" / "Escalas.docx"
    pasta_saida = base_path / "saidas"
    pasta_saida.mkdir(exist_ok=True)

    doc = DocxTemplate(modelo_path)

    blocos = []

    # Agrupa por Lugar
    for lugar, grupo in df.groupby("Lugar"):

        bloco = {
            "evento": grupo["evento"].iloc[0],
            "lugar": lugar,
            "colaboradores": grupo[
                ["nome_colaborador", "CATEGORIA", "VALOR"]
            ].to_dict(orient="records"),
        }

        blocos.append(bloco)

    contexto = {
        "blocos": blocos
    }

    doc.render(contexto)

    caminho_saida = pasta_saida / "escalas.docx"
    doc.save(caminho_saida)

    return caminho_saida
