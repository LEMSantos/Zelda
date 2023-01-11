from typing import Union, Sequence

from pygame.image import load as load_image
from pygame.sprite import Sprite, Group
from pygame.math import Vector2
from pygame import Surface

from zelda.src.settings import SCREEN_WIDTH, SCREEN_HEIGHT, BASE_PATH
from zelda.src.elements.player import Player


class CameraGroup(Group):
    """Câmera simples para movimentação do player.

    Classe que repesenta a câmera baseada na posição em Y dos sprites.
    Levando em consideração a posição do player. Todo o cenário se move
    na tela em relação a posição do player, que está sempre no centro.
    """

    def __init__(self, *sprites: Union[Sprite, Sequence[Sprite]]):
        """Inicializa a classe da câmera com o offset inicial, que por
        padrão é um Vector2D com x=0 e y=0.
        """
        super().__init__(*sprites)

        self.offset = Vector2()
        self.floor_surface = load_image(
            f"{BASE_PATH}/graphics/tilemap/ground.png").convert()
        self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))

    def custom_draw(self, surface: Surface, player: Player) -> None:
        """Desenha todos os sprites na tela.

        Os sprites serão desenhados de forma que aqueles que estiverem
        embaixo da tela serão desenhados por último, garantindo que
        serão desenhados por cima dos anteriores.

        Args:
            surface (Surface):
                superfície em que os sprites serão desenhados
            player (Player):
                Instância do player que será considerado
        """
        # Cria o offset da camera em relação ao player para mantê-lo no
        # centro da tela sempre
        self.offset.x = player.rect.centerx - SCREEN_WIDTH // 2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT // 2

        # Desenha o sprite do chão antes de qualquer outro sprite
        surface.blit(
            self.floor_surface,
            self.floor_rect.topleft - self.offset,
        )

        # Ordena os sprites pela posição em y para garantir que aqueles
        # que estiverem abaixo serão desenhados por cima para uma falsa
        # ilusão de 3D
        ordered_sprites = sorted(
            self.sprites(),
            key=lambda s: s.rect.centery,
        )

        for sprite in ordered_sprites:
            offset_rect = sprite.rect.copy()
            offset_rect.center -= self.offset

            surface.blit(sprite.image, offset_rect)
