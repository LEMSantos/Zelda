import os
from typing import Callable, Dict, List, Tuple, Union
from collections import defaultdict

from pygame.sprite import AbstractGroup
from pygame.math import Vector2

from zelda.src.settings import MONSTER_DATA, BASE_PATH, TILESIZE, MAP_GRID
from zelda.src.core.utils import import_folder
from zelda.src.elements.entity import Entity
from zelda.src.core.timer import Timer


class Enemy(Entity):
    """Sprite que representa um inimigo.

    Essa classe é responsável por lidar com as animações, ações
    realizadas e cooldowns.
    """

    def __init__(self,
                 position: Tuple[float, float],
                 groups: Union[List[AbstractGroup], AbstractGroup],
                 handle_collisions: Callable[[str], None],
                 monster_name: str,
                 get_player_pos: Callable) -> None:
        """Inicializa a classe do inimigo.

        Args:
            position (Tuple[float, float]):
                posição do inimigo na tela, em pixels
            groups (Union[List[AbstractGroup], AbstractGroup]):
                grupos que o inimigo deve pertencer quando for utilizado
                no jogo
            handle_collisions (Callable[[str], None]):
                função para lidar com as colisões horizontais e
                verticais
            monster_name (str):
                nome do monstro considerado
            get_player_pos (Callable):
                função para pegar a posição atual do player
        """
        # Setup geral
        self.sprite_type = "enemy"
        self.monster_name = monster_name
        self.__get_player_pos = get_player_pos

        # Estatísticas
        self.__dict__.update(MONSTER_DATA[monster_name])

        super().__init__(position, groups, handle_collisions)

        # Animações
        self.animation_speed = 0.15

         # Colisão
        self.hitbox = self.rect.copy().inflate((0, -10))

        # Interação com o player
        self.can_attack = True

    def _import_assets(self) -> None:
        """importa todos os assets do inimigo, condicional ao nome dele,
        presentes no pasta graphics/monsters/{monster_name} e gera um
        dicionário de animações.
        """
        assets_path = f"{BASE_PATH}/graphics/monsters/{self.monster_name}"

        _dirs = [name for name in os.listdir(assets_path)
                 if os.path.isdir(f"{assets_path}/{name}")]

        self._animations = defaultdict(list)

        for name in _dirs:
            self._animations[name] = import_folder(f"{assets_path}/{name}")

    def _get_status(self) -> None:
        """Atualiza o status do inimigo de acordo com a ação executada.
        """
        distance, _ = self.__get_player_distance_direction()

        if (
            distance <= self.attack_radius
            and self.can_attack
        ):
            if self.status != "attack":
                self._frame_index = 0

            self.status = "attack"
        elif distance <= self.notice_radius:
            self.status = "move"
        else:
            self.status = "idle"

    def _create_cooldowns(self) -> Dict[str, Timer]:
        """Cria os cooldowns necessários para o inimigo

        Returns:
            Dict[str, Timer]:
                retorna um dicionário com o nome do cooldown e o timer
                correspondente
        """
        return {
            "attack": Timer(1000, self.__reset_attack),
        }

    def _animate(self, animation_speed: float) -> None:
        """Gera as animações do inimigo de acordo com o status

        Args:
            animation_speed (float): velocidade de execução da animação
        """
        animation = self._animations[self.status]

        self._frame_index += animation_speed

        if self._frame_index >= len(animation):
            if self.status == "attack":
                self.can_attack = False

            self._frame_index = 0

        self.image = animation[int(self._frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def __get_direction(self,
                        player_pos: Vector2,
                        enemy_pos: Vector2) -> Vector2:
        """Gera o vetor de direção normalizada entre o inimigo e o
        player.

        Args:
            player_pos (Vector2): posição do player
            enemy_pos (Vector2): posição do inimigo

        Returns:
            Vector2: vetor de direção do inimigo para o player
        """
        distance = self.__get_distance(player_pos, enemy_pos)
        direction = Vector2()

        if distance > 0:
            direction = (player_pos - enemy_pos).normalize()

        return direction

    def __get_distance(self, player_pos: Vector2, enemy_pos: Vector2) -> float:
        """Calcula a distância entre o inimigo e o player

        Args:
            player_pos (Vector2): posição atual do player
            enemy_pos (Vector2): posição atual do inimigo

        Returns:
            float: retorna a distância
        """
        return enemy_pos.distance_to(player_pos)

    def __get_player_distance_direction(self) -> Tuple[float, Vector2]:
        """Calcula tanto a distância do player quanto o vetor de
        direção.

        Returns:
            Tuple[float, Vector2]: tupla com a distância e a direção
        """
        player_pos = self.__get_player_pos()

        if not player_pos or not hasattr(self, "rect"):
            return float('inf'), Vector2()

        player_pos = Vector2(player_pos)
        enemy_pos = Vector2(self.rect.center)

        return (
            self.__get_distance(player_pos, enemy_pos),
            self.__get_direction(player_pos, enemy_pos),
        )

    def __reset_attack(self) -> None:
        """Permite ao inimigo atacar novamente.
        """
        self.can_attack = True

    def __actions(self) -> None:
        """Realiza a ação correspondente ao status do inimigo.
        """
        if self.status == "attack":
            self._cooldowns["attack"].activate()
            print("attacking")
        elif self.status == "move":
            _, self.direction = self.__get_player_distance_direction()
        else:
            self.direction = Vector2()

    def update(self) -> None:
        """Atualiza o sprite dos inimigos
        """
        self.__actions()
        super().update()
