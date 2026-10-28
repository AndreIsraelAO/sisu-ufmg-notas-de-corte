from importlib.resources import files


def caminho(nome="notas_corte_final.csv"):
    """Caminho de um CSV do dataset (ex.: 'notas_corte.csv')."""
    p = files(__package__) / "data" / nome
    if not p.is_file():
        raise FileNotFoundError(f"{nome} não existe; veja os arquivos em {files(__package__) / 'data'}")
    return p
