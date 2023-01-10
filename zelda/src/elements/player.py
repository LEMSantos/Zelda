from dataclasses import dataclass
from typing import Callable, List, Tuple, Union

from pygame.math import Vector2
from pygame.image import load as load_image
from pygame.sprite import Sprite, AbstractGroup
from pygame import K_UP, K_DOWN, K_LEFT, K_RIGHT
from pygame.key import get_pressed as get_pressed_keys

from zelda.src.settings import BASE_PATH


@dataclass
class Movement:
    """Classe para representar um movimento possível do player.

    Args:
        key (int): código da tecla mapeada no movimento
        axis (str): eixo do movimento do player, 'x' ou 'y'
        direction (int): direção do movimento no eixo
        status (str): nome do movimento, 'up', 'down', 'left' ou 'right'
    """
    key: int
    axis: str
    direction: int
    status: str


class Player(Sprite):
    """Sprite que representa o player do jogo.

    Essa classe lida com as animações e captura de entradas feitas pelo
    usuário para o player.
    """

    __ALLOWED_MOVEMENTS: List[Movement] = [
        Movement(key=K_UP, axis="y", direction=-1, status="up"),
        Movement(key=K_DOWN, axis="y", direction=1, status="down"),
        Movement(key=K_LEFT, axis="x", direction=-1, status="left"),
        Movement(key=K_RIGHT, axis="x", direction=1, status="right"),
    ]

    def __init__(self,
                 position: Tuple[float, float],
                 groups: Union[List[AbstractGroup], AbstractGroup],
                 handle_collisions: Callable[[str], None]) -> None:
        """Faz o setup básico do player

        Args:
            position (Tuple[float, float]):
                posição do player na tela, em pixels
            groups (Union[List[AbstractGroup], AbstractGroup]):
                grupos que o player deve pertencer quando for utilizado
                no jogo
            handle_collisions (Callable[[str], None]):
                função para lidar com as colisões horizontais e
                verticais
        """
        super().__init__(groups)

        # Setup
        self.__handle_collisions = handle_collisions

        # Gráfico
        self.image = load_image(f"{BASE_PATH}/graphics/test/player.png")
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect(topleft=position)

        # Movimento
        self.direction = Vector2()
        self.speed = 5

        # Ações
        self.status = "down_idle"

        # Colisão
        self.hitbox = self.rect.copy().inflate((0, -26))

    def __handle_inputs(self) -> None:
        """Captura as entradas do usuário para o player
        """
        self.direction = Vector2()
        pressed_keys = get_pressed_keys()

        # Seta a direção e o status de acordo com a tecla pressionada
        for movement in self.__ALLOWED_MOVEMENTS:
            if pressed_keys[movement.key]:
                setattr(self.direction, movement.axis, movement.direction)
                self.status = movement.status

    def __move(self) -> None:
        """Método para movimentar o player na tela
        """
        _direction = self.direction

        # Garante que a velocidade é constante em qualquer direção
        if self.direction.magnitude() > 0:
            _direction = self.direction.normalize()

        # Movimenta horizontalmente
        self.hitbox.centerx += round(_direction.x * self.speed)
        self.rect.centerx = self.hitbox.centerx
        self.__handle_collisions("horizontal")

        # Movimenta verticalmente
        self.hitbox.centery += round(_direction.y * self.speed)
        self.rect.centery = self.hitbox.centery
        self.__handle_collisions("vertical")

    def update(self) -> None:
        """Método para atulização do sprite. Esse método é utilizado
        pelo grupo que ele pertence.
        """
        self.__handle_inputs()
        self.__move()
