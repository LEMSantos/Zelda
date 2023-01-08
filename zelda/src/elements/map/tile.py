from typing import List, Tuple, Union

from pygame.image import load as load_image
from pygame.sprite import Sprite, AbstractGroup

from zelda.src.settings import BASE_PATH


class Tile(Sprite):
    """Sprite que representa um único quadrado do jogo.
    """

    def __init__(self,
                 position: Tuple[float, float],
                 groups: Union[List[AbstractGroup], AbstractGroup]) -> None:
        """Faz o setup básico do tile

        Args:
            position (Tuple[float, float]):
                posição do tile na tela, em pixels
            groups (Union[List[AbstractGroup], AbstractGroup]):
                grupos que o tile deve pertencer quando for utilizado no
                jogo
        """
        super().__init__(groups)

        # Gráfico
        self.image = load_image(f"{BASE_PATH}/graphics/test/rock.png")
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect(topleft=position)

        # Colisão
        self.hitbox = self.rect.copy().inflate((-5, -5))
