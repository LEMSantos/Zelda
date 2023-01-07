from typing import List, Tuple, Union

from pygame.image import load as load_image
from pygame.sprite import Sprite, AbstractGroup

from zelda.src.settings import BASE_PATH


class Player(Sprite):
    """Sprite que representa o player do jogo.

    Essa classe lida com as animações e captura de entradas feitas pelo
    usuário para o player.
    """

    def __init__(self,
                 position: Tuple[float, float],
                 groups: Union[List[AbstractGroup], AbstractGroup]) -> None:
        """Faz o setup básico do player

        Args:
            position (Tuple[float, float]):
                posição do player na tela, em pixels
            groups (Union[List[AbstractGroup], AbstractGroup]):
                grupos que o player deve pertencer quando for utilizado
                no jogo
        """
        super().__init__(groups)

        self.image = load_image(f"{BASE_PATH}/graphics/test/player.png")
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect(topleft=position)
