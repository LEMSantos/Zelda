from random import choice
from typing import List, Sequence, Tuple, Union

from pygame.sprite import AbstractGroup, Sprite
from pygame import Surface

from zelda.src.core.utils import import_folder, reflect_images
from zelda.src.settings import BASE_PATH


class AnimationPlayer:

    def __init__(self) -> None:
        _path = f"{BASE_PATH}/graphics/particles"

        self.__frames = {
            # magic
            "flame": import_folder(f"{_path}/flame/frames"),
            "aura": import_folder(f"{_path}/aura"),
            "heal": import_folder(f"{_path}/heal/frames"),

            # attacks
            "claw": import_folder(f"{_path}/claw"),
            "slash": import_folder(f"{_path}/slash"),
            "sparkle": import_folder(f"{_path}/sparkle"),
            "leaf_attack": import_folder(f"{_path}/leaf_attack"),
            "thunder": import_folder(f"{_path}/thunder"),

            # monster deaths
            "squid": import_folder(f"{_path}/smoke_orange"),
            "raccoon": import_folder(f"{_path}/raccoon"),
            "spirit": import_folder(f"{_path}/nova"),
            "bamboo": import_folder(f"{_path}/bamboo"),

            # leafs
            "leaf": (
                import_folder(f"{_path}/leaf1"),
                import_folder(f"{_path}/leaf2"),
                import_folder(f"{_path}/leaf3"),
                import_folder(f"{_path}/leaf4"),
                import_folder(f"{_path}/leaf5"),
                import_folder(f"{_path}/leaf6"),
                reflect_images(import_folder(f"{_path}/leaf1")),
                reflect_images(import_folder(f"{_path}/leaf2")),
                reflect_images(import_folder(f"{_path}/leaf3")),
                reflect_images(import_folder(f"{_path}/leaf4")),
                reflect_images(import_folder(f"{_path}/leaf5")),
                reflect_images(import_folder(f"{_path}/leaf6")),
            ),
        }

    def create_particles(
        self,
        name: str,
        position: Tuple[int, int],
        groups: Union[AbstractGroup, Sequence[AbstractGroup]]
    ) -> None:
        animation_frames = self.__frames[name]

        if isinstance(self.__frames[name], tuple):
            animation_frames = choice(self.__frames[name])

        ParticleEffect(
            position=position,
            animation_frames=animation_frames,
            groups=groups,
        )


class ParticleEffect(Sprite):
    """Classe para lidar com o efeito de partículas.

    Esse efeito geralmente é utilizado para indicar algo sendo destruido
    ou sumindo da tela, a exemplo de magia.
    """

    def __init__(self,
                 position: Tuple[int, int],
                 animation_frames: List[Surface],
                 groups: Union[AbstractGroup, Sequence[AbstractGroup]]) -> None:
        """Inicializa a classe de efeito.

        Args:
            position (Tuple[int, int]):]
                posição de renderização do efeito
            animation_frames (List[Surface]):
                lista dos frames que compõem a animação do efeito
            groups (Union[AbstractGroup, Sequence[AbstractGroup]]):
                grupos em que o sprite será colocado enquanto existir
        """
        super().__init__(groups)

        self.__frame_index = 0
        self.__animation_speed = 0.15
        self.__frames = animation_frames
        self.image = animation_frames[self.__frame_index]
        self.rect = self.image.get_rect(center=position)

    def __animate(self) -> None:
        self.__frame_index += self.__animation_speed

        if self.__frame_index >= len(self.__frames):
            self.kill()
        else:
            self.image = self.__frames[int(self.__frame_index)]

    def update(self) -> None:
        """Atualiza o efeito até o tempo de duração acabar e o sprite
        ser removido da tela.
        """
        self.__animate()
