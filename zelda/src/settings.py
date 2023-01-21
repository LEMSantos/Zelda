from pathlib import Path
from typing import Dict, Union

BASE_PATH = str(Path().resolve()).replace('/zelda', '')

GAME_TITLE = "Zelda"

SCREEN_WIDTH: int = 1280
SCREEN_HEIGHT: int = 720
FPS: int = 60
TILESIZE: int = 64

# Cores gerais
WATER_COLOR: str = "#71ddee"
TEXT_COLOR: str = "#EEEEEE"

# Parâmetros da UI
UI_BAR_HEIGHT: int = 20
UI_HEALTH_BAR_WIDTH: int = 200
UI_ENERGY_BAR_WIDTH: int = 140
UI_ITEM_BOX_SIZE: int = 80
UI_FONT: str = f"{BASE_PATH}/graphics/font/joystix.ttf"
UI_FONT_SIZE: int = 18

# Cores da UI
UI_BG_COLOR: str = "#222222"
UI_BORDER_COLOR: str = "#111111"
UI_HEALTH_COLOR: str = "red"
UI_ENERGY_COLOR: str = "blue"
UI_BORDER_COLOR_ACTIVE: str = "gold"

# Armas
WEAPON_DATA: Dict[str, Dict[str, Union[int, str]]] = {
    "sword": {"cooldown": 100, "damage": 15, "graphic": "sword/full.png"},
    "lance": {"cooldown": 400, "damage": 30, "graphic": "lance/full.png"},
    "axe": {"cooldown": 300, "damage": 20, "graphic": "axe/full.png"},
    "rapier": {"cooldown": 50, "damage": 8, "graphic": "rapier/full.png"},
    "sai": {"cooldown": 80, "damage": 10, "graphic": "sai/full.png"},
}

# Magias
MAGIC_DATA: Dict[str, Dict[str, Union[int, str]]] = {
    "flame": {"strength": 50, "cost": 20, "graphic": "flame/fire.png"},
    "heal": {"strength": 20, "cost": 10, "graphic": "heal/heal.png"},
}


# Inimigos
MONSTER_DATA: Dict[str, Dict[str, Union[int, str]]] = {
    "squid": {
        "health": 100,
        "exp": 100,
        "damage": 20,
        "attack_type": "slash",
        "attack_sound": f"{BASE_PATH}/audio/attack/slash.wav",
        "speed": 3,
        "resistance": 3,
        "attack_radius": 80,
        "notice_radius": 360,
    },
    "raccoon": {
        "health": 300,
        "exp": 250,
        "damage": 40,
        "attack_type": "claw",
        "attack_sound": f"{BASE_PATH}/audio/attack/claw.wav",
        "speed": 2,
        "resistance": 3,
        "attack_radius": 120,
        "notice_radius": 400,
    },
    "spirit": {
        "health": 100,
        "exp": 110,
        "damage": 8,
        "attack_type": "thunder",
        "attack_sound": f"{BASE_PATH}/audio/attack/fireball.wav",
        "speed": 4,
        "resistance": 3,
        "attack_radius": 60,
        "notice_radius": 350,
    },
    "bamboo": {
        "health": 70,
        "exp": 120,
        "damage": 6,
        "attack_type": "leaf_attack",
        "attack_sound": f"{BASE_PATH}/audio/attack/slash.wav",
        "speed": 3,
        "resistance": 3,
        "attack_radius": 50,
        "notice_radius": 300,
    },
}

PLAYER_MAX_STATS: Dict[str, int] = {
    "health": 300,
    "energy": 140,
    "attack": 20,
    "magic": 10,
    "speed": 12,
}
