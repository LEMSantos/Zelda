import pygame

from zelda.src.levels.abstract_level import AbstractLevel
from zelda.src.settings import WORLD_MAP, TILESIZE
from zelda.src.elements.player import Player
from zelda.src.elements.map.tile import Tile


class MainLevel(AbstractLevel):
    """Level principal, o primeiro quando o jogo começa.
    """

    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__(screen)

        # Setup dos grupos de sprites
        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()

        # Setup dos sprites
        self.__create_map()

    def __create_map(self) -> None:
        """Método que instância os elementos do mapa em seus devidos
        grupos de sprites.
        """
        for i, row in enumerate(WORLD_MAP):
            for j, tile in enumerate(row):
                x = j * TILESIZE
                y = i * TILESIZE

                if tile == "p":
                    self.player = Player(
                        position=(x, y),
                        groups=[self.visible_sprites],
                        handle_collisions=self.__handle_collisions,
                    )

                    continue

                if tile == "x":
                    Tile((x, y), [self.visible_sprites, self.obstacle_sprites])

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
                    if self.player.direction.x > 0:
                        self.player.hitbox.right = sprite.hitbox.left

                    if self.player.direction.x < 0:
                        self.player.hitbox.left = sprite.hitbox.right

                    self.player.rect.centerx = self.player.hitbox.centerx

                # Impede os objetos de se transporem verticalmente
                if direction == "vertical":
                    if self.player.direction.y > 0:
                        self.player.hitbox.bottom = sprite.hitbox.top

                    if self.player.direction.y < 0:
                        self.player.hitbox.top = sprite.hitbox.bottom

                    self.player.rect.centery = self.player.hitbox.centery

    def run(self) -> None:
        self.visible_sprites.update()
        self.visible_sprites.draw(self.display_surface)
