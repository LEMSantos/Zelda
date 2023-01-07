import pygame

from zelda.src.levels.abstract_level import AbstractLevel


class MainLevel(AbstractLevel):

    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__(screen)

        # Setup dos grupos de sprites
        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()

    def run(self) -> None:
        pass
