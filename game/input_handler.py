# game/input_handler.py
import pygame
import sys
from game.game_state import game_state  # ✅ 改從 `game_state.py` 導入
from character.movement import handle_player_movement
from combat.combat import handle_attacks
from character.upgrade import handle_upgrade_selection
from ui.menus import handle_menu_click  # 確保從 `ui.menus` 導入

def handle_input():
    """處理鍵盤 & 滑鼠輸入"""
    global game_state

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # 🔹 處理鍵盤輸入
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if game_state == "playing":
                    game_state = "paused"
                elif game_state == "paused":
                    game_state = "playing"

            # 處理玩家攻擊
            handle_attacks(event)

            # 處理升級選單（數字鍵選擇升級）
            handle_upgrade_selection(event)

        # 🔹 處理滑鼠輸入（點擊選單按鈕）
        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_menu_click(event)

        # 🔹 處理玩家移動
        handle_player_movement(event)