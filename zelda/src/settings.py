from pathlib import Path

BASE_PATH = Path().resolve()

GAME_TITLE = "Zelda"

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
TILESIZE = 64

WEAPON_DATA = {
    "sword": {"cooldown": 100, "damage": 15, "graphic": "sword/full.png"},
    "lance": {"cooldown": 400, "damage": 30, "graphic": "lance/full.png"},
    "axe": {"cooldown": 300, "damage": 20, "graphic": "axe/full.png"},
    "rapier": {"cooldown": 50, "damage": 8, "graphic": "rapier/full.png"},
    "sai": {"cooldown": 80, "damage": 10, "graphic": "sai/full.png"},
}
