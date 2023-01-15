from typing import Sequence, Tuple, Union

from pygame import Surface
from pygame.sprite import AbstractGroup, Sprite
from pygame.mask import from_surface as mask_from_surface

from zelda.src.core.timer import Timer


class Particle(Sprite):
    """Classe para lidar com o efeito de partículas.

    Esse efeito geralmente é utilizado para indicar algo sendo destruido
    ou sumindo da tela, a exemplo de magia.
    """

    def __init__(self,
                 position: Tuple[int, int],
                 surface: Surface,
                 groups: Union[AbstractGroup, Sequence[AbstractGroup]],
                 duration: int = 200) -> None:
        """Incializa a classe de efeito.

        Args:
            position (Tuple[int, int]): posição de renderização
            surface (Surface): superfície em que o efeito será aplicado
            groups (Union[AbstractGroup, Sequence[AbstractGroup]]):
                grupos em que o sprite será colocado enquanto existir
            duration (int, optional):
                tempo de duração do efeito. 200 por padrão
        """
        super().__init__(groups)

        self.rect = surface.get_rect(topleft=position)

        self.animation_timer = Timer(duration)
        self.animation_timer.activate()

        mask_surf = mask_from_surface(surface)
        new_surf = mask_surf.to_surface()

        new_surf.set_colorkey((0, 0, 0))

        self.image = new_surf

    def update(self) -> None:
        """Atualiza o efeito até o tempo de duração acabar e o sprite
        ser removido da tela.
        """
        self.animation_timer.update()

        if not self.animation_timer.active:
            self.kill()
