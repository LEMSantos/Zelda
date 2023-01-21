from typing import Any, Dict, List

from pygame.image import load as load_image
from pygame.draw import rect as draw_rect
from pygame.display import get_surface
from pygame import Rect, Surface
from pygame.font import Font

from zelda.src.elements.player import Player
from zelda.src.settings import (
    BASE_PATH,
    MAGIC_DATA,
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
        self.__weapon_graphics = self.__load_graphics(
            prefix="graphics/weapons",
            data=WEAPON_DATA,
        )

        self.__magic_graphics = self.__load_graphics(
            prefix="graphics/particles",
            data=MAGIC_DATA,
        )

    @staticmethod
    def __load_graphics(prefix: str,
                        data: Dict[str, Any]) -> List[Surface]:
        """Importa os gráficos de um determinado elemento

        Args:
            prefix (str): prefixo utilizado para localizar a pasta
            data (Dict[str, Any]): dados dos elementos

        Returns:
            List[Surface]: lista de superfícies a partir das imagens
        """
        return [
            load_image(f"{BASE_PATH}/{prefix}/{item['graphic']}")
            for item in data.values()
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

    def show_overlay(self,
                     left: int,
                     top: int,
                     index: int,
                     highlight_box: bool,
                     graphics: List[Surface]) -> None:
        """Mostra na tela uma caixa de seleção.

        Args:
            left (int): posição x do overlay
            top (int): posição y do overlay
            index (int): gráfico utilizado atualmente no overlay.
            highlight_box (bool): define se a caixa deve ser destacada.
            graphics (List[Surface]):
                lista de superfícies gráficas que devem ser consideradas
                no overlay
        """
        bg_rect = self.show_selection_box(
            left=left,
            top=top,
            highlight=highlight_box,
        )

        _surf = graphics[index]
        _rect = _surf.get_rect(center=bg_rect.center)

        self.screen.blit(_surf, _rect)

    def display(self, player: Player) -> None:
        """Constrói toda a UI do game utilizando as informações do
        player.

        Args:
            player (Player): instância do player
        """
        self.show_bar(
            current=player.health,
            max_amount=player.get_stats("health"),
            bg_rect=self.health_bar_rect,
            color=UI_HEALTH_COLOR,
        )

        self.show_bar(
            current=player.energy,
            max_amount=player.get_stats("energy"),
            bg_rect=self.energy_bar_rect,
            color=UI_ENERGY_COLOR,
        )

        self.show_exp(player.exp)

        self.show_overlay(
            left=10,
            top=self.screen.get_height() - UI_ITEM_BOX_SIZE - 10,
            index=player.weapon_index,
            highlight_box=player.switching_weapon,
            graphics=self.__weapon_graphics,
        )
        self.show_overlay(
            left=80,
            top=self.screen.get_height() - UI_ITEM_BOX_SIZE - 5,
            index=player.magic_index,
            highlight_box=player.switching_magic,
            graphics=self.__magic_graphics,
        )
