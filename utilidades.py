import re

from datetime import datetime, date

def dia_semana(data_str: str) -> str:
    dias = [
        "Segunda",
        "Terça",
        "Quarta",
        "Quinta",
        "Sexta",
        "Sábado",
        "Domingo",
    ]

    data = datetime.strptime(data_str, "%d/%m/%Y")
    return dias[data.weekday()]

def limpar_nome_arquivo(nome: str) -> str:
    nome = re.sub(r'[\\/:"*?<>|]+', '-', nome)
    nome = re.sub(r'\s+', ' ', nome).strip()
    return nome or "cliente"

def formato_br_data(data_valor) -> str:
    if isinstance(data_valor, date):
        return data_valor.strftime("%d/%m/%Y")

    if isinstance(data_valor, str):
        data = datetime.strptime(data_valor, "%Y-%m-%d")
        return data.strftime("%d/%m/%Y")

    return ""

