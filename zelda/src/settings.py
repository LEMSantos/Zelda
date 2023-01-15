from pathlib import Path

BASE_PATH = Path().resolve()

GAME_TITLE = "Zelda"

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
TILESIZE = 64

# Cores gerais
WATER_COLOR = "#71ddee"
TEXT_COLOR = "#EEEEEE"

# Parâmetros da UI
UI_BAR_HEIGHT = 20
UI_HEALTH_BAR_WIDTH = 200
UI_ENERGY_BAR_WIDTH = 140
UI_ITEM_BOX_SIZE = 80
UI_FONT = f"{BASE_PATH}/graphics/font/joystix.ttf"
UI_FONT_SIZE = 18

# Cores da UI
UI_BG_COLOR = "#222222"
UI_BORDER_COLOR = "#111111"
UI_HEALTH_COLOR = "red"
UI_ENERGY_COLOR = "blue"
UI_BORDER_COLOR_ACTIVE = "gold"

# Armas
WEAPON_DATA = {
    "sword": {"cooldown": 100, "damage": 15, "graphic": "sword/full.png"},
    "lance": {"cooldown": 400, "damage": 30, "graphic": "lance/full.png"},
    "axe": {"cooldown": 300, "damage": 20, "graphic": "axe/full.png"},
    "rapier": {"cooldown": 50, "damage": 8, "graphic": "rapier/full.png"},
    "sai": {"cooldown": 80, "damage": 10, "graphic": "sai/full.png"},
}

# Magias
MAGIC_DATA = {
    "flame": {"strength": 5,"cost": 20,"graphic":"flame/fire.png"},
    "heal" : {"strength": 20,"cost": 10,"graphic":"heal/heal.png"},
}


# Inimigos
MONSTER_DATA = {
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
        "exp":120,
        "damage":6,
        "attack_type": "leaf_attack",
        "attack_sound":f"{BASE_PATH}/audio/attack/slash.wav",
        "speed": 3,
        "resistance": 3,
        "attack_radius": 50,
        "notice_radius": 300,
    },
}
