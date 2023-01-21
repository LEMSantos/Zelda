from itertools import chain
from random import choice as random_choice, randint
from typing import Tuple, Union

from pygame import Surface
from pygame.math import Vector2
from pygame.sprite import Group, groupcollide

from zelda.src.core.camera import CameraGroup
from zelda.src.core.particle_effect import AnimationPlayer
from zelda.src.core.utils import import_csv, import_folder
from zelda.src.elements.enemy import Enemy
from zelda.src.elements.entity import Entity
from zelda.src.elements.magic import MagicPlayer
from zelda.src.elements.player import Player
from zelda.src.elements.tile import Tile
from zelda.src.elements.ui import UI
from zelda.src.elements.weapon import Weapon
from zelda.src.levels.abstract_level import AbstractLevel
from zelda.src.settings import BASE_PATH, TILESIZE


class MainLevel(AbstractLevel):
    """Level principal, o primeiro quando o jogo começa.
    """

    def __init__(self, screen: Surface) -> None:
        super().__init__(screen)

        # Setup dos grupos de sprites
        self.visible_sprites = CameraGroup()
        self.obstacle_sprites = Group()
        self.attackable_sprites = Group()
        self.attack_sprites = Group()

        # Setup dos sprites
        self.__create_map()

        # Sprites de ataque
        self.current_attack = None
        self.current_attack_type = None

        # Interface do usuário
        self.ui = UI()

        # Particles
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)

    def __create_map(self) -> None:
        """Método que instância os elementos do mapa em seus devidos
        grupos de sprites.
        """
        # Mapeia os layouts com o posicionamento dos elementos em cada
        # camada do mapa
        layouts = {
            "boundary": import_csv(f"{BASE_PATH}/map/map_FloorBlocks.csv"),
            "grass": import_csv(f"{BASE_PATH}/map/map_Grass.csv"),
            "object": import_csv(f"{BASE_PATH}/map/map_Objects.csv"),
            "entities": import_csv(f"{BASE_PATH}/map/map_Entities.csv"),
        }

        # Mapeia os assets representando cada elemento especificado
        # no layout
        graphics = {
            "grass": import_folder(f"{BASE_PATH}/graphics/grass"),
            "object": import_folder(f"{BASE_PATH}/graphics/objects"),
        }

        enemy_names = {
            "390": "bamboo",
            "391": "spirit",
            "392": "raccoon",
            "393": "squid",
        }

        for style, layout in layouts.items():
            for i, row in enumerate(layout):
                for j, tile in enumerate(row):
                    if tile != "-1":
                        x = j * TILESIZE
                        y = i * TILESIZE

                        # Cria barreiras invisíveis para que o player
                        # não saia do mapa
                        if style == "boundary":
                            Tile(
                                position=(x, y),
                                groups=[self.obstacle_sprites],
                                sprite_type="invisible",
                            )

                        # Cria os objetos que são obstáculos visíveis
                        # para o player
                        if style in ["grass", "object"]:
                            groups = [
                                self.visible_sprites,
                                self.obstacle_sprites,
                            ]

                            if style == "object":
                                surface = graphics[style][int(tile)]
                            else:
                                groups.append(self.attackable_sprites)
                                surface = random_choice(graphics[style])

                            Tile(
                                position=(x, y),
                                groups=groups,
                                sprite_type=style,
                                surface=surface,
                            )

                        if style == "entities":
                            if tile == "394":
                                self.player = Player(
                                    position=(x, y),
                                    groups=[self.visible_sprites],
                                    handle_collisions=self.__handle_collisions,
                                    create_attack=self.__create_attack,
                                    destroy_attack=self.__destroy_attack,
                                    create_magic=self.__create_magic,
                                )

                            if tile in enemy_names.keys():
                                Enemy(
                                    position=(x, y),
                                    groups=[
                                        self.visible_sprites,
                                        self.attackable_sprites,
                                    ],
                                    handle_collisions=self.__handle_collisions,
                                    monster_name=enemy_names[tile],
                                    get_player_pos=self.__get_player_pos,
                                    inflict_damage_on_player=self.__inflict_damage_on_player,
                                    trigger_death_particles=self.__trigger_death_particles,
                                )

    def __create_attack(self) -> None:
        """Cria a arma selecionada pelo player na tela.
        """
        self.current_attack_type = "weapon"
        self.current_attack = Weapon(
            self.player,
            [self.visible_sprites, self.attack_sprites],
        )

    def __destroy_attack(self) -> None:
        """Destroi o ataque corrente se ele já tiver sido previamente
        criado.
        """
        if self.current_attack:
            self.current_attack.kill()

        self.current_attack = None
        self.current_attack_type = None

    def __create_magic(self, style: str, strength: int, cost: int) -> None:
        """Gera os efeitos da magia.

        Args:
            style (str): identificador da animação
            strength (int): força de uso da magia
            cost (int): custo de uso da magia
        """
        self.current_attack_type = "magic"

        if style == "flame":
            self.magic_player.flame(
                player=self.player,
                cost=cost,
                groups=[self.visible_sprites, self.attack_sprites],
            )

        if style == "heal":
            self.magic_player.heal(
                player=self.player,
                strength=strength,
                cost=cost,
                groups=[self.visible_sprites],
            )

    def __handle_collisions(self,
                            target: Entity,
                            direction: str) -> None:
        """Método para lidar com colisões.

        Colisões podem ser horizontais ou verticais, cada uma delas
        possui uma forma de tratamento diferente e não devem ser
        executadas simultaneamente no mesmo ciclo.

        Args:
            direction (str):
                direção da colisão, 'vertical' ou 'horizontal'
        """
        for sprite in self.obstacle_sprites.sprites():
            if (hasattr(sprite, "hitbox")
                    and target.hitbox.colliderect(sprite.hitbox)):
                # Impede os objetos de se transporem horizontalmente
                if direction == "horizontal":
                    # Movendo para a direita
                    if target.direction.x > 0:
                        target.hitbox.right = sprite.hitbox.left

                    # Movendo para a esquerda
                    if target.direction.x < 0:
                        target.hitbox.left = sprite.hitbox.right

                    target.rect.centerx = target.hitbox.centerx

                # Impede os objetos de se transporem verticalmente
                if direction == "vertical":
                    # Movendo para baixo
                    if target.direction.y > 0:
                        target.hitbox.bottom = sprite.hitbox.top

                    # Movendo para cima
                    if target.direction.y < 0:
                        target.hitbox.top = sprite.hitbox.bottom

                    target.rect.centery = target.hitbox.centery

    def __get_player_pos(self) -> Union[Tuple[int, int], None]:
        """Retorna a posição corrente do player no mapa.

        Returns:
            Union[Tuple[int, int], None]: posição atual do player
        """
        if hasattr(self, "player"):
            return self.player.rect.center

    def __inflict_damage_on_player(self,
                                   damage: float,
                                   attack_type: str) -> None:
        """Aplica dano ao player.

        Args:
            damage (float): dano infligido
            attack_type (str): tipo da animação de ataque
        """
        self.player.receive_damage(damage)

        self.animation_player.create_particles(
            name=attack_type,
            position=self.player.rect.center,
            groups=[self.visible_sprites],
        )

    def __trigger_death_particles(self,
                                  position: Tuple[int, int],
                                  particle_type: str) -> None:
        """Cria a animação de morte dos monstros.

        Args:
            position (Tuple[int, int]):
                posição onde o efeito deve ser renderizado
            particle_type (str):
                identificador para o efeito
        """
        self.animation_player.create_particles(
            name=particle_type,
            position=position,
            groups=[self.visible_sprites],
        )

    def __player_attack_logic(self) -> None:
        """Implementa a lógica de ataque do player.
        """
        if self.attack_sprites:
            collide_list = chain(*groupcollide(
                self.attack_sprites,
                self.attackable_sprites,
                False,
                False,
            ).values())

            for collided in collide_list:
                if isinstance(collided, Tile):
                    collided.kill()

                    offset = Vector2(0, 75)
                    for _ in range(randint(3, 6)):
                        self.animation_player.create_particles(
                            name="leaf",
                            position=collided.rect.center - offset,
                            groups=[self.visible_sprites],
                        )

                if isinstance(collided, Enemy):
                    collided.receive_damage(
                        self.player,
                        self.current_attack_type,
                    )

                    if not collided.alive:
                        self.player.exp += collided.exp

    def run(self) -> None:
        self.visible_sprites.update()
        self.visible_sprites.custom_draw(self.display_surface, self.player)
        self.__player_attack_logic()

        self.ui.display(self.player)
