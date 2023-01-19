from os import walk
from csv import reader
from typing import Any, Dict, List, Union

from pygame.transform import flip as flip_surface
from pygame.image import load as load_image
from pygame import Surface


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


def import_folder(
    path: str,
    get_dict: bool = False
) -> Union[Dict[str, Surface], List[Surface]]:
    """Importa os assets presentes em uma pasta.

    Args:
        path (str):
            caminho para a pasta com as imagens
        get_dict (bool, optional):
            define se o retorno da função será como uma lista ou como um
            dicionário. False por padrão.

    Returns:
        Union[Dict[str, Surface], List[Surface]]:
            o retorno pode ser uma lista de superfícies ou um dicionário
            com o nome da subpasta como chave e uma lista de superfícies
            como o valor.
    """
    # Função para lidar com o tratamento do dicionário
    def __handle_dict(surfaces: dict, name: str, surf: Surface) -> None:
        surfaces[name] = surf

    # Função para lidar com o tratamento da lista
    def __handle_list(surfaces: list, _: Any, surf: Surface) -> None:
        surfaces.append(surf)

    # Define qual tratamento deve ser utilizado baseado no parâmetro
    # get_dict
    surfaces, handle_add = (
        ({}, __handle_dict)
        if get_dict else ([], __handle_list)
    )

    for _, __, img_files in walk(path):
        for image in sorted(img_files):
            handle_add(
                surfaces,
                image.replace(".png", ""),
                load_image(f"{path}/{image}").convert_alpha()
            )

    return surfaces


def reflect_images(frames: List[Surface]) -> List[Surface]:
    return [flip_surface(frame, True, False) for frame in frames]
