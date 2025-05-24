# character/movement.py
# character/movement.py
import pygame
from character.character import player
from settings import DEFAULT_WIDTH, DEFAULT_HEIGHT #  <<<===  修改為匯入 DEFAULT_WIDTH, DEFAULT_HEIGHT

def handle_player_movement():
    """處理玩家移動（WASD / 方向鍵）"""
    keys = pygame.key.get_pressed()
    dx = int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) - int(keys[pygame.K_LEFT] or keys[pygame.K_a])
    dy = int(keys[pygame.K_DOWN] or keys[pygame.K_s]) - int(keys[pygame.K_UP] or keys[pygame.K_w])

    if dx or dy:
        # 計算移動方向，確保對角線移動時不會變快
        magnitude = (dx ** 2 + dy ** 2) ** 0.5
        dx /= magnitude if magnitude else 1
        dy /= magnitude if magnitude else 1

    # 檢查裝備是否影響速度
    base_speed = player.speed
    if any(e["name"] == "Wind Boots" for e in player.equipment):
        base_speed *= 1.15  # `Wind Boots` 讓玩家速度增加 15%

    # 更新玩家位置
    player.x += dx * base_speed
    player.y += dy * base_speed

    # 確保玩家不會跑出螢幕外
    player.x = max(0, min(DEFAULT_WIDTH - player.size, player.x)) #  <<<===  修改為 DEFAULT_WIDTH
    player.y = max(0, min(DEFAULT_HEIGHT - player.size, player.y)) #  <<<===  修改為 DEFAULT_HEIGHT