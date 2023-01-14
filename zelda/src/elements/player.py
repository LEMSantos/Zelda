import os
from dataclasses import dataclass
from collections import defaultdict
from typing import Callable, List, Tuple, Union

from pygame.math import Vector2
from pygame.sprite import Sprite, AbstractGroup
from pygame import K_UP, K_DOWN, K_LEFT, K_RIGHT, K_SPACE, K_LCTRL, K_q
from pygame.key import get_pressed as get_pressed_keys

from zelda.src.core.timer import Timer
from zelda.src.settings import BASE_PATH, WEAPON_DATA, PLAYER_BASE_STATS
from zelda.src.core.utils import import_folder


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


class Action:
    """Classe para representar uma ação possível do player

    Args:
        key (int): código da tecla mapeada na ação
        name (str): nome da ação que será executada
    """
    key: int
    name: str


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
                 handle_collisions: Callable[[str], None],
                 create_attack: Callable,
                 destroy_attack: Callable) -> None:
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
        self.__import_assets()
        self.__handle_collisions = handle_collisions

        # Ações
        self.status = "down_idle"
        self.__frame_index = 0

        # Gráfico
        self.image = self.__animations[self.status][self.__frame_index]
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect(topleft=position)

        # Movimento
        self.direction = Vector2()

        # Colisão
        self.hitbox = self.rect.copy().inflate((0, -26))

        # Cooldowns
        self.__cooldowns = {
            "attack": Timer(400, destroy_attack),
            "change_weapon": Timer(200),
        }

        # Armas
        self.__create_attack = create_attack
        self.weapon_index = 0
        self.weapon = list(WEAPON_DATA.keys())[self.weapon_index]

        # Estatísticas
        self.health = PLAYER_BASE_STATS["health"]
        self.energy = PLAYER_BASE_STATS["energy"]
        self.speed = PLAYER_BASE_STATS["speed"]
        self.exp = 100

    def __import_assets(self) -> None:
        """importa todos os assets do player presentes na pasta
        graphics/player e gera um dicionário de animações.
        """
        assets_path = f"{BASE_PATH}/graphics/player"

        _dirs = [name for name in os.listdir(assets_path)
                 if os.path.isdir(f"{assets_path}/{name}")]

        self.__animations = defaultdict(list)

        for name in _dirs:
            self.__animations[name] = import_folder(f"{assets_path}/{name}")

    def __handle_inputs(self) -> None:
        """Captura as entradas do usuário para o player
        """
        self.direction = Vector2()
        pressed_keys = get_pressed_keys()

        if not self.__cooldowns["attack"].active:
            # Seta a direção e o status de acordo com a tecla pressionada
            for movement in self.__ALLOWED_MOVEMENTS:
                if pressed_keys[movement.key]:
                    setattr(self.direction, movement.axis, movement.direction)
                    self.status = movement.status

            if pressed_keys[K_SPACE] or pressed_keys[K_LCTRL]:
                self.__frame_index = 0
                self.__cooldowns["attack"].activate()
                self.__create_attack()

            if (
                pressed_keys[K_q]
                and not self.__cooldowns["change_weapon"].active
            ):
                weapons_list = list(WEAPON_DATA.keys())

                self.weapon_index = (self.weapon_index + 1) % len(weapons_list)
                self.weapon = weapons_list[self.weapon_index]

                self.__cooldowns["change_weapon"].activate()

    def __get_status(self) -> None:
        """Atualiza o status do player de acordo com a ação executada.
        """
        if self.direction.magnitude() == 0:
            self.status = self.status.split("_")[0]
            self.status = f"{self.status}_idle"

        if self.__cooldowns["attack"].active:
            self.status = self.status.split("_")[0]
            self.status = f"{self.status}_attack"

    def __update_cooldowns(self):
        """Atualiza todos os timers utilizados pelo player.
        """
        for cooldown in self.__cooldowns.values():
            cooldown.update()

    def __move(self) -> None:
        """Método para movimentar o player na tela.
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

    def __animate(self) -> None:
        """Executa a animação do player de acordo com o status atual.
        """
        self.__frame_index += 0.1
        self.__frame_index %= len(self.__animations[self.status])

        self.image = self.__animations[self.status][int(self.__frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def update(self) -> None:
        """Método para atulização do sprite. Esse método é utilizado
        pelo grupo que ele pertence.
        """
        self.__handle_inputs()
        self.__get_status()
        self.__update_cooldowns()

        self.__move()
        self.__animate()
