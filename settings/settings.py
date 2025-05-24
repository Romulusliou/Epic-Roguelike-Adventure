# settings.py
import pygame
import os
import math # Added for math.radians

# ==================== 視窗設定 ====================
# These are defaults; init_settings() currently uses dynamic fullscreen size.
DEFAULT_WIDTH = 1920
DEFAULT_HEIGHT = 1080
FULLSCREEN = True # This can be used by main.py if dynamic sizing is not preferred

# ==================== 字型設定 ====================
FONT_DIR = "assets/fonts"
DEFAULT_FONT_FILENAME = "NotoSansTC-VariableFont_wght.ttf"
FALLBACK_FONT_FILENAME_MSJH = "msjh.ttc"
FALLBACK_FONT_NAME_ARIAL = "arial" # For Pygame SysFont
EMOJI_FONT_FILENAME = "seguiemj.ttf" # Ensure this font is in assets/fonts
FALLBACK_EMOJI_FONT_NAME_ARIAL = "arial" # For Pygame SysFont

FONT_SIZE_NORMAL = 40
FONT_SIZE_EQUIP = 30
FONT_SIZE_UPGRADE = 30
FONT_SIZE_UPGRADE_SMALL = 24

# Construct absolute paths for fonts
# Assumes settings.py is in a 'settings' subdirectory of the game's root project directory
GAME_ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
FONT_PATH_NORMAL = os.path.join(GAME_ROOT_DIR, FONT_DIR, DEFAULT_FONT_FILENAME)
FONT_PATH_EMOJI = os.path.join(GAME_ROOT_DIR, FONT_DIR, EMOJI_FONT_FILENAME)

# ==================== 顏色定義 ====================
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
RED = (255, 0, 0)
PINK = (255, 192, 203)
BROWN = (139, 69, 19)
LIGHT_GREEN = (144, 238, 144)
LIGHT_YELLOW = (255, 255, 224)
LIGHT_BLUE = (173, 216, 230)
LIGHT_CYAN = (224, 255, 255)
PURPLE = (128, 0, 128)
DARK_RED = (139, 0, 0)
ENEMY_TANK_COLOR = (100, 100, 100) # Custom color for tank

COLOR_DICT = {
    "BLACK": BLACK, "WHITE": WHITE, "GREEN": GREEN, "ORANGE": ORANGE,
    "BLUE": BLUE, "YELLOW": YELLOW, "CYAN": CYAN, "RED": RED,
    "PINK": PINK, "BROWN": BROWN, "LIGHT_GREEN": LIGHT_GREEN,
    "LIGHT_YELLOW": LIGHT_YELLOW, "LIGHT_BLUE": LIGHT_BLUE,
    "LIGHT_CYAN": LIGHT_CYAN, "PURPLE": PURPLE, "DARK_RED": DARK_RED,
    "ENEMY_TANK_COLOR": ENEMY_TANK_COLOR
}

def get_color(name):
    """取得顏色，若名稱不存在則回傳 BLACK"""
    return COLOR_DICT.get(name.upper(), BLACK)

# ==================== Game Parameters ====================

# Player
BASE_PLAYER_SPEED = 5
PLAYER_SIZE = 40 
PLAYER_DAMAGE_COOLDOWN = 500 # ms

# Weapons
SWORD_DURATION = 300  # ms
SWORD_RANGE = 80      # pixels
SWORD_FAN_ANGLE_DEGREES = 60 # degrees

BULLET_COOLDOWN = 300  # ms
BULLET_SPEED = 10     # pixels per frame/tick
BULLET_COUNT = 3      # bullets per shot
BULLET_SPREAD_DEGREES = 30 # degrees

# Effects
MUZZLE_FLASH_DURATION = 100 # ms

# Enemy
ENEMY_STATS = {
    "normal": {"speed": 2, "size": 20, "color": RED, "max_hp": 100},
    "elite": {"speed": 3, "size": 20, "color": PURPLE, "max_hp": 150},
    "swift": {"speed": 4, "size": 18, "color": CYAN, "max_hp": 80},
    "tank": {"speed": 1, "size": 30, "color": ENEMY_TANK_COLOR, "max_hp": 200},
    "healer": {"speed": 2, "size": 22, "color": LIGHT_BLUE, "max_hp": 120},
    "bomber": {"speed": 2, "size": 24, "color": ORANGE, "max_hp": 100},
    "summoner": {"speed": 1.5, "size": 26, "color": PINK, "max_hp": 130},
    "boss": {"speed": 1, "size": 40, "color": DARK_RED, "max_hp": 500}
}

# Wave Management
MAX_ENEMIES_ON_SCREEN = 10
DEFAULT_MAX_WAVES = 10
WAVE_ENEMY_TYPES = {
    1: ["normal"],
    3: ["normal", "elite", "swift"],
    5: ["normal", "elite", "swift", "tank"],
    7: ["normal", "elite", "swift", "tank", "healer"],
    9: ["normal", "elite", "swift", "tank", "healer", "bomber", "summoner"]
}

# ==================== Initialization Function ====================
def init_settings():
    """Initializes Pygame (if not already), screen dimensions, and fonts."""
    if not pygame.get_init():
        pygame.init()
        print("✅ settings.py: pygame.init() called.")
    else:
        print("ℹ️ settings.py: pygame already initialized.")

    try:
        infoObject = pygame.display.Info()
        WIDTH, HEIGHT = infoObject.current_w, infoObject.current_h
        print(f"✅ Detected screen resolution: {WIDTH}x{HEIGHT} (Fullscreen/Current Desktop)")
    except pygame.error as e:
        print(f"❌ Pygame display error when getting display info: {e}. Falling back to default dimensions: {DEFAULT_WIDTH}x{DEFAULT_HEIGHT}.")
        WIDTH, HEIGHT = DEFAULT_WIDTH, DEFAULT_HEIGHT
    
    font = None
    equip_font = None
    upgrade_font = None
    upgrade_font_small = None

    try:
        font = pygame.font.Font(FONT_PATH_NORMAL, FONT_SIZE_NORMAL)
    except Exception as e:
        print(f"❌ Main font ({FONT_PATH_NORMAL}) load failed: {e}")
        try:
            font = pygame.font.Font(FALLBACK_FONT_FILENAME_MSJH, FONT_SIZE_NORMAL)
            print(f"✅ Loaded fallback MSJH for main font.")
        except Exception as e_fallback:
            print(f"❌ Fallback MSJH font load failed: {e_fallback}")
            font = pygame.font.SysFont(FALLBACK_FONT_NAME_ARIAL, FONT_SIZE_NORMAL)
            print(f"✅ Loaded system Arial for main font.")

    try:
        equip_font = pygame.font.Font(FONT_PATH_EMOJI, FONT_SIZE_EQUIP)
    except Exception as e:
        print(f"❌ Emoji font ({FONT_PATH_EMOJI}) load failed: {e}")
        equip_font = pygame.font.SysFont(FALLBACK_EMOJI_FONT_NAME_ARIAL, FONT_SIZE_EQUIP)
        print(f"✅ Loaded system Arial for equipment/emoji font.")
    
    try:
        upgrade_font = pygame.font.Font(FONT_PATH_NORMAL, FONT_SIZE_UPGRADE)
    except Exception as e:
        print(f"⚠️ Upgrade font load failed ({FONT_PATH_NORMAL} size {FONT_SIZE_UPGRADE}): {e}. Using main font as fallback.")
        upgrade_font = font 
    
    try:
        upgrade_font_small = pygame.font.Font(FONT_PATH_NORMAL, FONT_SIZE_UPGRADE_SMALL)
    except Exception as e:
        print(f"⚠️ Small upgrade font load failed ({FONT_PATH_NORMAL} size {FONT_SIZE_UPGRADE_SMALL}): {e}. Using main font as fallback.")
        upgrade_font_small = font 

    print(f"✅ settings.py: init_settings() completed. Screen: {WIDTH}x{HEIGHT}. Main font loaded: {font is not None}")
    return WIDTH, HEIGHT, font, equip_font, upgrade_font, upgrade_font_small
