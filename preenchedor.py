from docxtpl import DocxTemplate
from pathlib import Path
from datetime import datetime


def preencher_modelo(
    dados: dict,
    nome_modelo: str,
    pasta_modelos: str = "modelos",
    pasta_saida: str = "saidas",
    sufixo_timestamp: bool = True,
    nome_saida = "nome_padrão"
) -> Path:
    """
    Preenche um modelo DOCX usando docxtpl.

    :param dados: dicionário com os dados para o template
    :param nome_modelo: nome do arquivo modelo (.docx)
    :param pasta_modelos: pasta onde estão os modelos
    :param pasta_saida: pasta onde o arquivo final será salvo
    :param sufixo_timestamp: adiciona timestamp ao nome do arquivo
    :return: Path do arquivo gerado
    """

    # Caminhos
    pasta_modelos = Path(pasta_modelos)
    pasta_saida = Path(pasta_saida)

    modelo_path = pasta_modelos / nome_modelo

    if not modelo_path.exists():
        raise FileNotFoundError(f"Modelo não encontrado: {modelo_path}")

    # Garante que a pasta de saída exista
    pasta_saida.mkdir(parents=True, exist_ok=True)

    # Nome do arquivo final
    nome_base = modelo_path.stem

    saida_path = pasta_saida / nome_saida

    # Carrega e renderiza o template
    doc = DocxTemplate(modelo_path)
    doc.render(dados)
    doc.save(saida_path)

    return saida_path
