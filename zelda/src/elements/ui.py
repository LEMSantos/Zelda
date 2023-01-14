from pygame.image import load as load_image
from pygame.draw import rect as draw_rect
from pygame.display import get_surface
from pygame.font import Font
from pygame import Rect

from zelda.src.elements.player import Player
from zelda.src.settings import (
    BASE_PATH,
    PLAYER_BASE_STATS,
    TEXT_COLOR,
    UI_BAR_HEIGHT,
    UI_BG_COLOR,
    UI_BORDER_COLOR,
    UI_BORDER_COLOR_ACTIVE,
    UI_ENERGY_BAR_WIDTH,
    UI_ENERGY_COLOR,
    UI_FONT,
    UI_FONT_SIZE,
    UI_HEALTH_BAR_WIDTH,
    UI_HEALTH_COLOR,
    UI_ITEM_BOX_SIZE,
    WEAPON_DATA,
)


class UI:
    """Classe que representa a Interface de Usuário do jogo.

    Essa classe é responsável por desenhar as barras de vida e energia,
    além da experiência do player e por fim as caixas de seleção da
    arma e da magia.
    """

    def __init__(self) -> None:
        """Faz o setup da UI do jogo.
        """
        # Setup geral
        self.screen = get_surface()
        self.font = Font(UI_FONT, UI_FONT_SIZE)

        # Setup das barras
        self.health_bar_rect = Rect(10, 10, UI_HEALTH_BAR_WIDTH, UI_BAR_HEIGHT)
        self.energy_bar_rect = Rect(10, 34, UI_ENERGY_BAR_WIDTH, UI_BAR_HEIGHT)

        # Setup das armas
        self.__weapon_graphics = [
            load_image(f"{BASE_PATH}/graphics/weapons/{item['graphic']}")
            for item in WEAPON_DATA.values()
        ]

    def show_bar(self,
                 current: float,
                 max_amount: float,
                 bg_rect: Rect,
                 color: str) -> None:
        """Desenha na tela as barras de stats do player.

        Args:
            current (float): valor atual da barra
            max_amount (float): valor máximo da barra
            bg_rect (Rect): coordenadas onde a barra será desenhada
            color (str): cor da barra
        """
        draw_rect(self.screen, UI_BG_COLOR, bg_rect, border_radius=5)

        health_percentage = current / max_amount
        current_rect = bg_rect.copy()
        current_rect.width = round(bg_rect.width * health_percentage)

        draw_rect(self.screen, color, current_rect, border_radius=5)
        draw_rect(self.screen, UI_BORDER_COLOR, bg_rect, 4, 5)

    def show_exp(self, exp: float) -> None:
        """Desenha na tela a informação de experiência do player

        Args:
            exp (float): experiência atual do player
        """
        padding = 20

        text_surf = self.font.render(f"{int(exp)}", False, TEXT_COLOR)

        x = self.screen.get_width() - padding
        y = self.screen.get_height() - padding
        text_rect = text_surf.get_rect(bottomright=(x, y))

        draw_rect(
            self.screen,
            UI_BG_COLOR,
            text_rect.inflate(20, 20),
            border_radius=5,
        )
        self.screen.blit(text_surf, text_rect)
        draw_rect(
            self.screen,
            UI_BORDER_COLOR,
            text_rect.inflate(20, 20),
            border_radius=5,
            width=4,
        )

    def show_selection_box(self,
                           left: int,
                           top: int,
                           highlight: bool = False) -> Rect:
        """Desenha na tela a caixa de seleção.

        Args:
            left (int): posição x da caixa
            top (int): posição y da caixa
            highlight (bool, optional):
                define se a caixa deve ser destacada através da mudança
                da cor da borda. False por padrão.

        Returns:
            Rect: coordenadas onde a caixa foi desenhada
        """
        bg_rect = Rect(left, top, UI_ITEM_BOX_SIZE, UI_ITEM_BOX_SIZE)

        draw_rect(self.screen, UI_BG_COLOR, bg_rect, border_radius=5)
        draw_rect(
            surface=self.screen,
            color=UI_BORDER_COLOR_ACTIVE if highlight else UI_BORDER_COLOR,
            rect=bg_rect,
            width=4,
            border_radius=5
        )

        return bg_rect

    def show_weapon_overlay(self, weapon_index: int, highlight_box: bool):
        """Mostra na tela a caixa de seleção da arma.

        Args:
            weapon_index (int): arma utilizada atualmente pelo player.
            highlight_box (bool): define se a caixa deve ser destacada.
        """
        bg_rect = self.show_selection_box(
            left=10,
            top=self.screen.get_height() - UI_ITEM_BOX_SIZE - 10,
            highlight=highlight_box,
        )

        weapon_surf = self.__weapon_graphics[weapon_index]
        weapon_rect = weapon_surf.get_rect(center=bg_rect.center)

        self.screen.blit(weapon_surf, weapon_rect)

    def display(self, player: Player) -> None:
        """Constrói toda a UI do game utilizando as informações do
        player.

        Args:
            player (Player): instância do player
        """
        self.show_bar(
            current=player.health,
            max_amount=PLAYER_BASE_STATS["health"],
            bg_rect=self.health_bar_rect,
            color=UI_HEALTH_COLOR,
        )

        self.show_bar(
            current=player.energy,
            max_amount=PLAYER_BASE_STATS["energy"],
            bg_rect=self.energy_bar_rect,
            color=UI_ENERGY_COLOR,
        )

        self.show_exp(player.exp)

        self.show_weapon_overlay(player.weapon_index, player.switching_weapon)
        self.show_selection_box(
            left=80,
            top=self.screen.get_height() - UI_ITEM_BOX_SIZE - 5
        )
