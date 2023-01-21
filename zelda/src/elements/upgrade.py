from pygame import K_RIGHT, K_LEFT, K_SPACE, Rect, Surface
from pygame.display import get_surface as get_display_surface
from pygame.draw import rect as draw_rect
from pygame.draw import line as draw_line
from pygame.font import Font
from pygame.key import get_pressed as get_pressed_keys
from pygame.math import Vector2

from zelda.src.core.timer import Timer
from zelda.src.elements.player import Player
from zelda.src.settings import (
    PLAYER_MAX_STATS,
    UI_FONT,
    UI_FONT_SIZE,
    UPGRADE_COST,
    UI_BG_COLOR,
    TEXT_COLOR,
    TEXT_COLOR_SELECTED,
    UPGRADE_BG_COLOR_SELECTED,
    UI_BORDER_COLOR,
    BAR_COLOR,
    BAR_COLOR_SELECTED,
)


class UpgradeMenu:

    def __init__(self, player: Player) -> None:
        self.screen = get_display_surface()
        self.player = player

        self.select_index = 0
        self.options = list(PLAYER_MAX_STATS.keys())
        self.font = Font(UI_FONT, UI_FONT_SIZE)
        self.selection_cooldown = Timer(300)

        self.box_height = self.screen.get_height() * 0.8
        self.box_width = self.screen.get_width() // (len(self.options) + 1)

        self.__create_items()

    def __input(self) -> None:
        if not self.selection_cooldown.active:
            keys = get_pressed_keys()

            if keys[K_RIGHT] and self.select_index < len(self.options) - 1:
                self.selection_cooldown.activate()
                self.select_index += 1
            elif keys[K_LEFT] and self.select_index > 0:
                self.selection_cooldown.activate()
                self.select_index -= 1

            if keys[K_SPACE]:
                self.selection_cooldown.activate()
                selected = self.options[self.select_index]

                if self.player.exp >= UPGRADE_COST[selected]:
                    value = self.player.get_stats(selected)

                    changed = self.player.set_stats(selected, value * 1.2)

                    if changed:
                        self.player.exp -= UPGRADE_COST[selected]
                        UPGRADE_COST[selected] = int(UPGRADE_COST[selected] * 1.4)

    def __create_items(self) -> None:
        self.item_list = []

        for i in range(len(self.options)):
            padding = self.screen.get_width() // len(self.options)

            left = (padding - self.box_width) // 2 + (i * padding)
            top = self.screen.get_height() * 0.1
            index = i

            self.item_list.append(Item(
                left=left,
                top=top,
                width=self.box_width,
                height=self.box_height,
                index=index,
                font=self.font,
            ))

    def display(self) -> None:
        self.__input()
        self.selection_cooldown.update()

        for index, item in enumerate(self.item_list):
            name = self.options[index]
            value = self.player.get_stats(name)
            max_value = PLAYER_MAX_STATS[name]
            cost = UPGRADE_COST[name]

            item.display(
                screen=self.screen,
                selection_num=self.select_index,
                name=name,
                value=value,
                max_value=max_value,
                cost=cost,
            )


class Item:

    def __init__(self,
                 left: int,
                 top: int,
                 width: int,
                 height: int,
                 index: int,
                 font: Font) -> None:
        self.rect = Rect(left, top, width, height)
        self.index = index
        self.font = font

    def display_names(self,
                      screen: Surface,
                      name: str,
                      cost: int,
                      selected: bool) -> None:
        color = TEXT_COLOR if not selected else TEXT_COLOR_SELECTED

        offset = Vector2(0, 20)

        title_surf = self.font.render(name, False, color)
        title_rect = title_surf.get_rect(
            midtop=Vector2(self.rect.midtop) + offset,
        )

        cost_surf = self.font.render(str(cost), False, color)
        cost_rect = cost_surf.get_rect(
            midbottom=Vector2(self.rect.midbottom) - offset,
        )

        screen.blit(title_surf, title_rect)
        screen.blit(cost_surf, cost_rect)

    def display_bar(self,
                    screen: Surface,
                    value: int,
                    max_value: int,
                    selected: bool) -> None:
        offset = Vector2(0, 60)

        top = Vector2(self.rect.midtop) + offset
        bottom = Vector2(self.rect.midbottom) - offset
        color = BAR_COLOR if not selected else BAR_COLOR_SELECTED

        full_height = bottom.y - top.y
        position = (value / max_value) * full_height

        slider_rect = Rect(0, 0, 30, 10)
        slider_rect.center = bottom - Vector2(0, position)

        draw_line(screen, color, top, bottom, 5)
        draw_rect(screen, color, slider_rect)

    def display(self,
                screen: Surface,
                selection_num: int,
                name: str,
                value: int,
                max_value: int,
                cost: int) -> None:
        selected = self.index == selection_num

        draw_rect(
            surface=screen,
            color=UI_BG_COLOR if not selected else UPGRADE_BG_COLOR_SELECTED,
            rect=self.rect,
        )
        draw_rect(
            surface=screen,
            color=UI_BORDER_COLOR,
            rect=self.rect,
            width=4,
        )

        self.display_names(screen, name, cost, selected)
        self.display_bar(screen, value, max_value, selected)
