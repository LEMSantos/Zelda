from typing import Dict, List, Tuple, Union

from pygame.sprite import AbstractGroup, Sprite
from pygame.image import load as load_image
from pygame.math import Vector2

from zelda.src.elements.player import Player
from zelda.src.settings import BASE_PATH


class Weapon(Sprite):
    """Sprite que representa uma arma no jogo.

    Esse sprite lida com a renderização condicional da arma, levando em
    consideração tando a direção, quanto a arma atualmente selecionada
    pelo player.
    """

    def __init__(self,
                 player: Player,
                 groups: Union[AbstractGroup, List[AbstractGroup]]):
        """Inicializa o sprite da arma selecionada pelo player.

        Args:
            player (Player):
                instância do player.
            groups (Union[AbstractGroup, List[AbstractGroup]]):
                grupos que o sprite deve estar.
        """
        super().__init__(groups)

        direction = player.status.split("_", 1)[0]
        position = self.__get_weapon_position(direction, player)

        # Gráficos
        self.image = load_image(
            self.__get_asset_path(direction, player.weapon)
        ).convert_alpha()

        self.rect = self.image.get_rect(**position)

    @staticmethod
    def __get_weapon_position(
        direction: str,
        player: Player,
    ) -> Dict[str, Tuple[float, float]]:
        """Gera a posição da arma referente ao posicionamento do player.

        Args:
            direction (str): direção que a arma deve ser posicionada.
            player (Player): instancia do player.

        Returns:
            Dict[str, Tuple[float, float]]:
                dicionário representando a posição de referência da arma
                e qual o valor essa posição deve ter.
        """
        y_offset = Vector2(0, 16)
        x_offset = Vector2(-10, 0)

        if direction == "right":
            return {"midleft": player.rect.midright + y_offset}

        if direction == "left":
            return {"midright": player.rect.midleft + y_offset}

        if direction == "up":
            return {"midbottom": player.rect.midtop + x_offset}

        return {"midtop": player.rect.midbottom + x_offset}

    @staticmethod
    def __get_asset_path(direction: str, weapon: str) -> str:
        """Monta o caminho para os assets da arma selecionada.

        Args:
            direction (str): direção que a arma deve ser posicionada.
            weapon (str): arma selecionada.

        Returns:
            str: caminho para a imagem correta da arma.
        """
        return f"{BASE_PATH}/graphics/weapons/{weapon}/{direction}.png"
