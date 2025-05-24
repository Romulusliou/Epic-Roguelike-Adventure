# combat/combat.py
import pygame
from character.character import player
from combat.weapon import WEAPONS
from combat.bullets import update_bullets, draw_bullets
from combat.explosions import update_explosions, draw_explosions
from ui.ui import add_floating_text
from game.game_state import enemies  # ✅ 改從 `game_state.py` 導入

def handle_attacks(event):
    """處理玩家攻擊輸入（空白鍵觸發所有武器）"""
    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        for weapon in player.weapons.values():
            if weapon:  # ✅ 只有解鎖的武器才會攻擊
                result = WEAPONS[weapon].attack(player)
                if isinstance(result, list):  # 霰彈槍等一次發射多個子彈
                    from combat.bullets import active_bullets
                    active_bullets.extend(result)

def update_combat():
    """更新戰鬥狀態（子彈 & 爆炸）"""
    if "sword" in player.weapons:
        WEAPONS["sword"].update_attack(player)
    
    update_bullets()  # ✅ 更新子彈狀態
    update_explosions()  # ✅ 更新爆炸狀態

def draw_combat(surface):
    """繪製戰鬥特效（子彈 & 爆炸）"""
    draw_bullets(surface)  # ✅ 繪製子彈
    draw_explosions(surface)  # ✅ 繪製爆炸動畫
