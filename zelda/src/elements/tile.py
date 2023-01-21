from typing import List, Tuple, Union

from pygame import Surface
from pygame.sprite import Sprite, AbstractGroup

from zelda.src.settings import TILESIZE, HITBOX_OFFSET


class Tile(Sprite):
    """Sprite que representa um único quadrado do jogo.
    """

    def __init__(self,
                 position: Tuple[float, float],
                 groups: Union[List[AbstractGroup], AbstractGroup],
                 sprite_type: str,
                 surface: Surface = Surface((TILESIZE, TILESIZE))) -> None:
        """Faz o setup básico do tile

        Args:
            position (Tuple[float, float]):
                posição do tile na tela, em pixels
            groups (Union[List[AbstractGroup], AbstractGroup]):
                grupos que o tile deve pertencer quando for utilizado no
                jogo
        """
        super().__init__(groups)

        self.sprite_type = sprite_type

        # Gráfico
        self.image = surface
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect(topleft=position)

        # Corrige o posicionamento do sprite para imagens maiores do que
        # 64 x 64 px
        if sprite_type == "object":
            self.rect = self.image.get_rect(
                topleft=(position[0], position[1] - TILESIZE),
            )

        # Colisão
        self.hitbox = self.rect.copy().inflate((0, HITBOX_OFFSET[sprite_type]))
