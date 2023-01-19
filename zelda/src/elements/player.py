import os
from dataclasses import dataclass
from collections import defaultdict
from typing import Callable, Dict, List, Tuple, Union

from pygame.math import Vector2
from pygame.sprite import AbstractGroup
from pygame.key import get_pressed as get_pressed_keys
from pygame import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_SPACE,
    K_LCTRL,
    K_q,
    K_e
)

from zelda.src.core.utils import import_folder
from zelda.src.elements.entity import Entity
from zelda.src.core.timer import Timer
from zelda.src.settings import (
    BASE_PATH,
    WEAPON_DATA,
    MAGIC_DATA,
)


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


class Player(Entity):
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
                 handle_collisions: Callable[["Entity", str], None],
                 create_attack: Callable,
                 destroy_attack: Callable,
                 create_magic: Callable) -> None:
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
            create_attack (Callable):
                função para criar o ataque na tela
            destroy_attack (Callable):
                função para destruir o ataque previamente criado
            create_magic (Callable):
                O mesmo que create_attack só que para magias
        """
        self.__create_attack = create_attack
        self.__destroy_attack = destroy_attack

        super().__init__(position, groups, handle_collisions)

        # Animações
        self.animation_speed = 0.1

        # Colisão
        self.hitbox = self.rect.copy().inflate((0, -26))

        # Armas
        self.weapon_index = 0
        self.weapon = list(WEAPON_DATA.keys())[self.weapon_index]

        # Magia
        self.__create_magic = create_magic
        self.magic_index = 0
        self.magic = list(MAGIC_DATA.keys())[self.magic_index]

        # Estatísticas
        self.stats = {
            "health": 100,
            "energy": 60,
            "attack": 10,
            "magic": 4,
            "speed": 6,
        }

        self.health = self.stats["health"]
        self.energy = self.stats["energy"]
        self.speed = self.stats["speed"]
        self.exp = 100

    def _import_assets(self) -> None:
        """importa todos os assets do player presentes na pasta
        graphics/player e gera um dicionário de animações.
        """
        assets_path = f"{BASE_PATH}/graphics/player"

        _dirs = [name for name in os.listdir(assets_path)
                 if os.path.isdir(f"{assets_path}/{name}")]

        self._animations = defaultdict(list)

        for name in _dirs:
            self._animations[name] = import_folder(f"{assets_path}/{name}")

    def __handle_inputs(self) -> None:
        """Captura as entradas do usuário para o player
        """
        self.direction = Vector2()
        pressed_keys = get_pressed_keys()

        if (
            not self._cooldowns["attack"].active
            and not self._cooldowns["magic"].active
        ):
            # Seta a direção e o status de acordo com a tecla pressionada
            for movement in self.__ALLOWED_MOVEMENTS:
                if pressed_keys[movement.key]:
                    setattr(self.direction, movement.axis, movement.direction)
                    self.status = movement.status

            if pressed_keys[K_SPACE]:
                weapon_cooldown = WEAPON_DATA[self.weapon]["cooldown"]
                self._cooldowns["attack"].extend_duration(weapon_cooldown)

                self._frame_index = 0
                self._cooldowns["attack"].activate()
                self.__create_attack()

            if pressed_keys[K_LCTRL]:
                self._frame_index = 0
                self._cooldowns["magic"].activate()
                self.__create_magic(
                    style=self.magic,
                    strength=(
                        MAGIC_DATA[self.magic]["strength"]
                        + self.stats["magic"]
                    ),
                    cost=MAGIC_DATA[self.magic]["cost"]
                )

            if (
                pressed_keys[K_q]
                and not self._cooldowns["change_weapon"].active
            ):
                weapons_list = list(WEAPON_DATA.keys())

                self.weapon_index = (self.weapon_index + 1) % len(weapons_list)
                self.weapon = weapons_list[self.weapon_index]

                self._cooldowns["change_weapon"].activate()

            if (
                pressed_keys[K_e]
                and not self._cooldowns["change_magic"].active
            ):
                magic_list = list(MAGIC_DATA.keys())

                self.magic_index = (self.magic_index + 1) % len(magic_list)
                self.magic = magic_list[self.magic_index]

                self._cooldowns["change_magic"].activate()

    def _get_status(self) -> None:
        """Atualiza o status do player de acordo com a ação executada.
        """
        if not hasattr(self, "status"):
            self.status = "down_idle"

        if self.direction.magnitude() == 0:
            self.status = self.status.split("_")[0]
            self.status = f"{self.status}_idle"

        if (
            self._cooldowns["attack"].active
            or self._cooldowns["magic"].active
        ):
            self.status = self.status.split("_")[0]
            self.status = f"{self.status}_attack"

    def _create_cooldowns(self) -> Dict[str, Timer]:
        """Cria os cooldowns necessários para o player

        Returns:
            Dict[str, Timer]:
                retorna um dicionário com o nome do cooldown e o timer
                correspondente
        """
        return {
            "attack": Timer(400, self.__destroy_attack),
            "magic": Timer(400),
            "change_weapon": Timer(200),
            "change_magic": Timer(200),
        }

    def __check_death(self) -> None:
        """Verifica se o player morreu e executa uma ação em caso positivo.
        """
        if self.health <= 0:
            print("morreu")
            exit(1)

    @property
    def switching_weapon(self) -> bool:
        """Propriedade indicando se o player está trocando de arma.
        """
        return self._cooldowns["change_weapon"].active

    @property
    def switching_magic(self) -> bool:
        """Propriedade indicando se o player está trocando de arma.
        """
        return self._cooldowns["change_magic"].active

    def get_full_weapon_damage(self) -> int:
        """Calcula o dano total do player ao utilizar armas.
        """
        base_damage = self.stats["attack"]
        weapon_damage = WEAPON_DATA[self.weapon]["damage"]

        return base_damage + weapon_damage

    def get_full_magic_damage(self) -> int:
        """Calcula o dano total do player ao utilizar magias.
        """
        return self.stats["magic"]

    def receive_damage(self, damage: float) -> None:
        """Computa o dano total infligido oo player.

        Args:
            damage (float): dano infligido ao player
        """
        if not self._cooldowns["invincibility"].active:
            self.health -= damage
            self._cooldowns["invincibility"].activate()

    def update(self) -> None:
        """Método para atualização do sprite. Esse método é utilizado
        pelo grupo que ele pertence.
        """
        self.__handle_inputs()
        super().update()

        # self.__check_death()
