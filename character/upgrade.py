# character/upgrade.py
import pygame
import random
from character.character import player
from ui.ui import draw_upgrade_overlay
from settings import get_color

# 定義可用的升級選項
UPGRADE_OPTIONS = [
    {
        "type": "stat",
        "subtype": "hp",
        "name": "強化生命值",
        "description": "永久增加 20 點生命值上限。",
        "effect": lambda: setattr(player, "max_hp", player.max_hp + 20),
        "level_required": 1,
        "display_color": "GREEN",
        "key_binding": pygame.K_1,
    },
    {
        "type": "stat",
        "subtype": "attack",
        "name": "強化攻擊力",
        "description": "永久增加 5 點攻擊力。",
        "effect": lambda: setattr(player, "attack_damage", player.attack_damage + 5),
        "level_required": 1,
        "display_color": "ORANGE",
        "key_binding": pygame.K_2,
    },
    {
        "type": "stat",
        "subtype": "speed",
        "name": "強化移動速度",
        "description": "永久提升 10% 移動速度。",
        "effect": lambda: setattr(player, "speed", player.speed * 1.1),
        "level_required": 2,
        "display_color": "YELLOW",
        "key_binding": pygame.K_3,
    },
    {
        "type": "stat",
        "subtype": "crit_rate",
        "name": "強化暴擊率",
        "description": "永久提升 5% 暴擊率。",
        "effect": lambda: setattr(player, "crit_rate", player.crit_rate + 0.05),
        "level_required": 4,
        "display_color": "RED",
        "key_binding": pygame.K_4,
    },
]

def get_available_upgrades():
    """篩選出符合等級需求的升級選項"""
    return [option for option in UPGRADE_OPTIONS if player.level >= option["level_required"]]

def handle_upgrade_selection(event):
    """處理升級選單輸入"""
    available_upgrades = get_available_upgrades()
    
    for option in available_upgrades:
        if event.type == pygame.KEYDOWN and event.key == option["key_binding"]:
            option["effect"]()  # 執行對應的升級效果
            return True  # 表示升級完成
    
    return False  # 尚未完成升級

def level_up():
    """當玩家升級時，顯示升級選單並等待玩家選擇"""
    available_upgrades = get_available_upgrades()
    if len(available_upgrades) > 3:
        upgrade_choices = random.sample(available_upgrades, 3)  # 隨機挑選 3 個選項
    else:
        upgrade_choices = available_upgrades
    
    upgrade_done = False
    while not upgrade_done:
        draw_upgrade_overlay(upgrade_choices, player.level)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if handle_upgrade_selection(event):
                upgrade_done = True
