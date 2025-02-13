# settings.py
import pygame
import os

# ==================== 視窗設定 ====================
DEFAULT_WIDTH = 1920
DEFAULT_HEIGHT = 1080
FULLSCREEN = True

# ==================== 字型設定 ====================
FONT_DIR = "assets/fonts"
DEFAULT_FONT_FILENAME = "NotoSansTC-VariableFont_wght.ttf"
FALLBACK_FONT_FILENAME_MSJH = "msjh.ttc"
FALLBACK_FONT_NAME_ARIAL = "arial"
EMOJI_FONT_FILENAME = "seguiemj.ttf"
FALLBACK_EMOJI_FONT_NAME_ARIAL = "arial"

FONT_SIZE_NORMAL = 40
FONT_SIZE_EQUIP = 30
FONT_SIZE_UPGRADE = 30
FONT_SIZE_UPGRADE_SMALL = 24

GAME_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_PATH_NORMAL = os.path.join(GAME_DIR, FONT_DIR, DEFAULT_FONT_FILENAME)
FONT_PATH_EMOJI = os.path.join(GAME_DIR, FONT_DIR, EMOJI_FONT_FILENAME)

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

COLOR_DICT = {
    "BLACK": BLACK, "WHITE": WHITE, "GREEN": GREEN, "ORANGE": ORANGE,
    "BLUE": BLUE, "YELLOW": YELLOW, "CYAN": CYAN, "RED": RED,
    "PINK": PINK, "BROWN": BROWN, "LIGHT_GREEN": LIGHT_GREEN,
    "LIGHT_YELLOW": LIGHT_YELLOW, "LIGHT_BLUE": LIGHT_BLUE,
    "LIGHT_CYAN": LIGHT_CYAN, "PURPLE": PURPLE, "DARK_RED": DARK_RED
}

def get_color(name):
    """取得顏色，若名稱不存在則回傳 BLACK"""
    return COLOR_DICT.get(name.upper(), BLACK)

def init_settings():
    print("✅ settings.py: init_settings() 被呼叫")
    return 1920, 1080, None, None, None, None

    pygame.init()
    infoObject = pygame.display.Info()
    WIDTH, HEIGHT = infoObject.current_w, infoObject.current_h

    # 載入主要字型
    try:
        font = pygame.font.Font(FONT_PATH_NORMAL, FONT_SIZE_NORMAL)
    except Exception as e:
        print(f"❌ 字型載入失敗: {e}")
        try:
            font = pygame.font.Font(FALLBACK_FONT_FILENAME_MSJH, FONT_SIZE_NORMAL)
        except:
            font = pygame.font.SysFont(FALLBACK_FONT_NAME_ARIAL, FONT_SIZE_NORMAL)

    # 載入 Emoji 字型
    try:
        equip_font = pygame.font.Font(FONT_PATH_EMOJI, FONT_SIZE_EQUIP)
    except:
        equip_font = pygame.font.SysFont(FALLBACK_EMOJI_FONT_NAME_ARIAL, FONT_SIZE_EQUIP)

    upgrade_font = pygame.font.Font(FONT_PATH_NORMAL, FONT_SIZE_UPGRADE)
    upgrade_font_small = pygame.font.Font(FONT_PATH_NORMAL, FONT_SIZE_UPGRADE_SMALL)

    return WIDTH, HEIGHT, font, equip_font, upgrade_font, upgrade_font_small
