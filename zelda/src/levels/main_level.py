from random import choice as random_choice

import pygame

from zelda.src.core.utils import import_csv, import_folder
from zelda.src.levels.abstract_level import AbstractLevel
from zelda.src.settings import BASE_PATH, TILESIZE
from zelda.src.core.camera import CameraGroup
from zelda.src.elements.player import Player
from zelda.src.elements.map.tile import Tile


class MainLevel(AbstractLevel):
    """Level principal, o primeiro quando o jogo começa.
    """

    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__(screen)

        # Setup dos grupos de sprites
        self.visible_sprites = CameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # Setup dos sprites
        self.__create_map()

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
        }

        # Mapeia os assets representando cada elemento especificado
        # no layout
        graphics = {
            "grass": import_folder(f"{BASE_PATH}/graphics/grass"),
            "object": import_folder(f"{BASE_PATH}/graphics/objects"),
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

                        # Cria os objectos que são obstáculos visíveis
                        # para o player
                        if style in ["grass", "object"]:
                            surface = (
                                random_choice(graphics[style])
                                if style == "grass" else
                                graphics[style][int(tile)]
                            )

                            Tile(
                                position=(x, y),
                                groups=[
                                    self.visible_sprites,
                                    self.obstacle_sprites,
                                ],
                                sprite_type=style,
                                surface=surface,
                            )

        self.player = Player(
            position=(2000, 1430),
            groups=[self.visible_sprites],
            handle_collisions=self.__handle_collisions,
        )

    def __handle_collisions(self, direction: str) -> None:
        """Método para lidar com colisões.

        Colisões podem ser horizontais ou verticais, cada uma delas
        possui uma forma de tratamento diferente e não devem ser
        executadas simultâneamente no mesmo ciclo.

        Args:
            direction (str):
                direção da colisão, 'vertical' ou 'horizontal'
        """
        for sprite in self.obstacle_sprites.sprites():
            if (hasattr(sprite, "hitbox")
                    and self.player.hitbox.colliderect(sprite.hitbox)):
                # Impede os objetos de se transporem horizontalmente
                if direction == "horizontal":
                    # Movendo para a direita
                    if self.player.direction.x > 0:
                        self.player.hitbox.right = sprite.hitbox.left

                    # Movendo para a esquerda
                    if self.player.direction.x < 0:
                        self.player.hitbox.left = sprite.hitbox.right

                    self.player.rect.centerx = self.player.hitbox.centerx

                # Impede os objetos de se transporem verticalmente
                if direction == "vertical":
                    # Movendo para baixo
                    if self.player.direction.y > 0:
                        self.player.hitbox.bottom = sprite.hitbox.top

                    # Movendo para cima
                    if self.player.direction.y < 0:
                        self.player.hitbox.top = sprite.hitbox.bottom

                    self.player.rect.centery = self.player.hitbox.centery

    def run(self) -> None:
        self.visible_sprites.update()
        self.visible_sprites.custom_draw(self.display_surface, self.player)
