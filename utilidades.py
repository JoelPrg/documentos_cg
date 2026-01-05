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
