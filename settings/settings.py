# settings.py
import pygame
import os

# ==================== Global Constants (if any are needed outside init_settings) ====================
# Example: GAME_DIR might be useful globally if other functions in settings need it.
GAME_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # Assuming settings.py is in settings/
ASSETS_DIR = os.path.join(GAME_DIR, "assets")
FONT_DIR = os.path.join(ASSETS_DIR, "fonts")

def init_settings():
    """
    Initializes Pygame, screen, fonts, and colors.
    Returns a dictionary containing all settings.
    """
    print("✅ settings.py: init_settings() is being called.")

    # ================= Initialization =====================
    pygame.init()
    # pygame.mixer.init() # Initialize the mixer for sound, if not already done

    # ✅ 自適應螢幕解析度（自動適應全螢幕）
    infoObject = pygame.display.Info()
    WIDTH, HEIGHT = infoObject.current_w, infoObject.current_h
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("穿越成為成最強冒險家")

    # ==================== Font Loading ====================
    # 🔥 Ensure correct path to fonts directory, assuming assets/fonts from the game's root
    # The original Game 1.py changes directory, which is not ideal.
    # It's better to construct absolute paths or paths relative to this file or a known root.
    # GAME_DIR is defined above, assuming settings.py is in a 'settings' subdirectory of the game root.
    
    font_path_noto_sans = os.path.join(FONT_DIR, "NotoSansTC-VariableFont_wght.ttf")

    try:
        main_font = pygame.font.Font(font_path_noto_sans, 40)
    except Exception as e:
        print(f"❌ NotoSansTC font loading failed: {e}")
        try:
            main_font = pygame.font.Font("msjh.ttc", 40)  # 微軟正黑體
            print("✅ Loaded fallback font: msjh.ttc")
        except Exception as e2:
            print(f"❌ Fallback msjh.ttc font loading failed: {e2}")
            main_font = pygame.font.SysFont("arial", 40)  # Backup
            print("✅ Loaded system default font: arial (main)")

    try:
        # Assuming seguiemj.ttf is also in the FONT_DIR
        emoji_font_path = os.path.join(FONT_DIR, "seguiemj.ttf")
        equip_font = pygame.font.Font(emoji_font_path, 30)
    except Exception as e:
        print(f"⚠️ Emoji font (seguiemj.ttf) not found: {e}. Using fallback.")
        equip_font = pygame.font.SysFont("arial", 30) # Backup
        print("✅ Loaded system default font: arial (equip)")

    try:
        upgrade_font = pygame.font.Font(font_path_noto_sans, 30)
    except Exception as e: # Fallback if NotoSansTC failed for main_font
        print(f"❌ NotoSansTC upgrade_font loading failed: {e}. Using main_font instance or fallback.")
        upgrade_font = main_font # Use the already loaded (or fallback) main_font logic
    
    try:
        upgrade_font_small = pygame.font.Font(font_path_noto_sans, 24)
    except Exception as e: # Fallback
        print(f"❌ NotoSansTC upgrade_font_small loading failed: {e}. Using main_font instance or fallback.")
        # Create a new font instance with smaller size if main_font is a specific file
        # or use a scaled version if that's preferred, though direct load is cleaner.
        if main_font.get_height() == 40: # Check if it's the expected main_font
             try:
                current_font_name = pygame.font.Font.get_fonts()[pygame.font.Font.get_fonts().index(main_font.name)]
                upgrade_font_small = pygame.font.Font(current_font_name, 24)
             except: # Absolute fallback
                upgrade_font_small = pygame.font.SysFont("arial", 24)
        else: # Fallback to a new SysFont instance if main_font was already a fallback
            upgrade_font_small = pygame.font.SysFont("arial", 24)


    # ==================== Color Definitions ====================
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

    settings_dict = {
        'screen': screen,
        'WIDTH': WIDTH,
        'HEIGHT': HEIGHT,
        'fonts': {
            'main': main_font,
            'equip': equip_font,
            'upgrade': upgrade_font,
            'upgrade_small': upgrade_font_small
        },
        'colors': COLOR_DICT,
        # Adding individual colors directly to the dict for easier access if preferred
        'BLACK': BLACK, 'WHITE': WHITE, 'GREEN': GREEN, 'ORANGE': ORANGE,
        'BLUE': BLUE, 'YELLOW': YELLOW, 'CYAN': CYAN, 'RED': RED,
        'PINK': PINK, 'BROWN': BROWN, 'LIGHT_GREEN': LIGHT_GREEN,
        'LIGHT_YELLOW': LIGHT_YELLOW, 'LIGHT_BLUE': LIGHT_BLUE,
        'LIGHT_CYAN': LIGHT_CYAN, 'PURPLE': PURPLE, 'DARK_RED': DARK_RED,
        'GAME_DIR': GAME_DIR, # Include if useful for other parts of the game
        'ASSETS_DIR': ASSETS_DIR,
        'FONT_DIR': FONT_DIR
    }
    print("✅ settings.py: init_settings() completed.")
    return settings_dict

# Example of a helper function that might use COLOR_DICT if it were global
# def get_color(name):
#    """取得顏色，若名稱不存在則回傳 BLACK"""
#    return COLOR_DICT.get(name.upper(), BLACK) # This would need COLOR_DICT to be global

if __name__ == '__main__':
    # This is for testing settings.py directly
    # In the actual game, main.py would import and call init_settings()
    settings = init_settings()
    print("\nSettings loaded:")
    print(f"Screen: {settings['screen']}")
    print(f"Resolution: {settings['WIDTH']}x{settings['HEIGHT']}")
    print(f"Main Font: {settings['fonts']['main']}")
    print(f"Colors Loaded: {len(settings['colors'])} colors in COLOR_DICT")

    # Example: Fill screen with a color and quit
    if settings['screen']:
        settings['screen'].fill(settings['BLUE'])
        pygame.display.flip()
        pygame.time.wait(2000) # Wait 2 seconds
    pygame.quit()
    print("\nSettings test finished.")
