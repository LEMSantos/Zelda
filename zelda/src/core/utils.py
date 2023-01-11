from csv import reader
from typing import Any, Dict, List, Union


def import_csv(path: str) -> List[List[str]]:
    """Importa um arquivo csv como uma matriz.

    Args:
        path (str): caminho para o arquivo csv

    Returns:
        List[List[str]]:
            matriz contendo a representação do arquivo após a leitura
    """
    with open(path) as level_map:
        layout = reader(level_map, delimiter=",")
        return [list(row) for row in layout]

