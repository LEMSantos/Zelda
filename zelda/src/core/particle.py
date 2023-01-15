from typing import Sequence, Tuple, Union

from pygame import Surface
from pygame.sprite import AbstractGroup, Sprite
from pygame.mask import from_surface as mask_from_surface

from zelda.src.core.timer import Timer


class Particle(Sprite):

    def __init__(self,
                 position: Tuple[int, int],
                 surface: Surface,
                 groups: Union[AbstractGroup, Sequence[AbstractGroup]],
                 duration: int = 200) -> None:
        super().__init__(groups)

        self.rect = surface.get_rect(topleft=position)

        self.animation_timer = Timer(duration)
        self.animation_timer.activate()

        mask_surf = mask_from_surface(surface)
        new_surf = mask_surf.to_surface()

        new_surf.set_colorkey((0, 0, 0))

        self.image = new_surf

    def update(self) -> None:
        self.animation_timer.update()

        if not self.animation_timer.active:
            self.kill()
