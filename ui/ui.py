# ui/ui.py
import pygame
import sys
import os


# 讓 Python 知道 settings.py 的路徑
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# 匯入 settings
from settings.settings import init_settings, get_color


# 初始化 settings（確保字型 & 屏幕尺寸載入）
WIDTH, HEIGHT, font, equip_font, upgrade_font, upgrade_font_small = init_settings()

# ================= Floating Text System =====================
floating_texts = []  # 每個元素：{"text": str, "pos": (x,y), "timer": ms}

def add_floating_text(text, pos, duration=1000):
    floating_texts.append({"text": text, "pos": pos, "timer": duration})

def update_floating_texts(dt):
    for obj in floating_texts[:]:
        obj["timer"] -= dt
        if obj["timer"] <= 0:
            floating_texts.remove(obj)

def draw_floating_texts(surface):
    for obj in floating_texts:
        draw_text(surface, obj["text"], obj["pos"], upgrade_font, "BLACK")

# =================== 通用繪製函式 ===================
def draw_text(surface, text, pos, font_used, color_name="WHITE"):
    """繪製文字，統一處理字型渲染"""
    text_surface = font_used.render(text, True, get_color(color_name))
    surface.blit(text_surface, pos)

def draw_overlay(surface, alpha=180):
    """繪製透明遮罩"""
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, alpha))
    surface.blit(overlay, (0, 0))

# ================= Upgrade Overlay =====================
def draw_upgrade_overlay(frame_surface, upgrade_options, player_level):
    draw_overlay(frame_surface, alpha=100)  # 使用統一的遮罩繪製函式

    box_width, box_height = 300, 200
    spacing = 50
    total_width = len(upgrade_options) * (box_width + spacing)
    start_x = (WIDTH - total_width) // 2
    start_y = (HEIGHT - box_height) // 2

    for i, option in enumerate(upgrade_options):
        box_x = start_x + i * (box_width + spacing)
        box_rect = pygame.Rect(box_x, start_y, box_width, box_height)
        pygame.draw.rect(frame_surface, get_color("BLACK"), box_rect, 2)

        box_color = get_color(option.get("display_color", "GREEN"))
        pygame.draw.rect(frame_surface, box_color, (box_x + 20, start_y + 20, box_width - 40, box_height - 80))

        draw_text(frame_surface, option["name"], (box_x + 20, start_y + box_height - 100), upgrade_font, "BLACK")
        draw_text(frame_surface, option["description"], (box_x + 20, start_y + box_height - 60), upgrade_font_small, "BLACK")

        key_prompt_text = f"Press {option['key_binding']}"
        draw_text(frame_surface, key_prompt_text, (box_x + 20, start_y + box_height - 30), upgrade_font, "BLACK")

    draw_text(frame_surface, "Choose upgrade", ((WIDTH - 200) // 2, start_y + box_height + 20), upgrade_font, "BLACK")

# ================= Pause Menu =====================
def draw_pause_menu(screen):
    draw_overlay(screen)  # 使用統一的遮罩繪製函式

    options = ["繼續遊戲", "設定", "回到首頁"]
    option_y = HEIGHT // 2 - 50
    for option in options:
        text_rect = font.render(option, True, get_color("WHITE")).get_rect(center=(WIDTH // 2, option_y))
        screen.blit(font.render(option, True, get_color("WHITE")), text_rect)
        option_y += 60
