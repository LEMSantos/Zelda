import pygame

from zelda.src.levels.abstract_level import AbstractLevel
from zelda.src.settings import WORLD_MAP, TILESIZE
from zelda.src.elements.player import Player
from zelda.src.elements.map.tile import Tile


class MainLevel(AbstractLevel):

    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__(screen)

        # Setup dos grupos de sprites
        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()

        # Setup dos sprites
        self.__create_map()

    def __create_map(self) -> None:
        for i, row in enumerate(WORLD_MAP):
            for j, tile in enumerate(row):
                x = j * TILESIZE
                y = i * TILESIZE

                if tile == 'p':
                    Player((x, y), [self.visible_sprites])
                    continue

                if tile == 'x':
                    Tile((x, y), [self.visible_sprites, self.obstacle_sprites])

    def run(self) -> None:
        self.visible_sprites.update()
        self.visible_sprites.draw(self.display_surface)
