from typing import List, Tuple, Union

from pygame.image import load as load_image
from pygame.sprite import Sprite, AbstractGroup

from zelda.src.settings import BASE_PATH


class Player(Sprite):

    def __init__(self,
                 position: Tuple[float, float],
                 groups: Union[List[AbstractGroup], AbstractGroup]) -> None:
        super().__init__(groups)

        self.image = load_image(
            f"{BASE_PATH}/graphics/test/player.png",
        ).convert_alpha()
        self.rect = self.image.get_rect(topleft=position)
