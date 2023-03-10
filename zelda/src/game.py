import sys

import pygame
from pygame.mixer import Sound

from zelda.src.levels.main_level import MainLevel
from zelda.src.settings import (
    BASE_PATH,
    GAME_TITLE,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS,
    WATER_COLOR,
)


class Game:
    """Implementa a lógica básica do jogo.

    A classe Game garante que os eventos serão capturados corretamente e
    também funciona como um wrapper para executar cada um dos níveis
    definidos para o jogo.
    """

    def __init__(self) -> None:
        """Monta a tela principal do jogo e inicializa o clock para a
        limitação de frames por segundo.
        """
        pygame.init()

        # Setup geral
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.current_level = MainLevel(self.screen)

        # Título da janela
        pygame.display.set_caption(GAME_TITLE)

        # Som
        main_sound = Sound(f"{BASE_PATH}/audio/main.ogg")
        main_sound.set_volume(0.1)
        main_sound.play(loops=-1)

    def __handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_m
            ):
                self.current_level.toggle_menu()

    def run(self) -> None:
        """Roda o loop principal necessário para trabalhar com pygame.

        O método run captura eventos gerados no decorrer do jogo, roda
        o nível atual que o player está jogando e garante a limitação
        de frames por segundo.
        """
        while True:
            self.__handle_events()

            self.screen.fill(WATER_COLOR)
            self.current_level.run()

            pygame.display.update()

            self.clock.tick(FPS)
