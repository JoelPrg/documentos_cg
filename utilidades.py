import re

from datetime import datetime

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
