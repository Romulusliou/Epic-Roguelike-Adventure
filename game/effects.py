# game/effects.py
import pygame
import random

# ==================== 螢幕震動效果 ====================

screen_shake_time = 0  # 震動剩餘時間（ms）
screen_shake_intensity = 0  # 震動強度

def trigger_screen_shake(duration, intensity):
    """觸發螢幕震動效果"""
    global screen_shake_time, screen_shake_intensity
    screen_shake_time = duration
    screen_shake_intensity = intensity

def apply_screen_shake(screen):
    """對螢幕應用震動效果"""
    global screen_shake_time
    if screen_shake_time > 0:
        offset_x = random.randint(-int(screen_shake_intensity), int(screen_shake_intensity))
        offset_y = random.randint(-int(screen_shake_intensity), int(screen_shake_intensity))
        screen.blit(screen, (offset_x, offset_y))
        screen_shake_time -= 1  # 遞減震動時間

# ==================== 槍口閃光效果 ====================

muzzle_flash_time = 0  # 槍口閃光剩餘時間（ms）
muzzle_flash_duration = 100  # 槍口閃光的持續時間（ms）

def trigger_muzzle_flash():
    """觸發槍口閃光效果"""
    global muzzle_flash_time
    muzzle_flash_time = pygame.time.get_ticks() + muzzle_flash_duration

def draw_muzzle_flash(surface, player_x, player_y):
    """繪製槍口閃光"""
    global muzzle_flash_time
    if pygame.time.get_ticks() < muzzle_flash_time:
        flash_radius = 15
        pygame.draw.circle(surface, (255, 165, 0), (player_x, player_y), flash_radius)

# ==================== 爆炸效果 ====================

explosions = []  # 爆炸清單，每個爆炸是一個字典 {"x", "y", "radius", "timer"}

def trigger_explosion(x, y, radius, duration):
    """觸發爆炸特效"""
    explosions.append({"x": x, "y": y, "radius": radius, "timer": duration})

def update_explosions():
    """更新爆炸效果的時間"""
    for explosion in explosions[:]:
        explosion["timer"] -= 1
        if explosion["timer"] <= 0:
            explosions.remove(explosion)

def draw_explosions(surface):
    """繪製爆炸動畫"""
    for explosion in explosions:
        alpha = max(50, 255 * (explosion["timer"] / 30))  # 動態透明度
        explosion_surface = pygame.Surface((explosion["radius"] * 2, explosion["radius"] * 2), pygame.SRCALPHA)
        pygame.draw.circle(explosion_surface, (255, 69, 0, alpha), (explosion["radius"], explosion["radius"]), explosion["radius"])
        surface.blit(explosion_surface, (explosion["x"] - explosion["radius"], explosion["y"] - explosion["radius"]))

# ==================== 整合更新 & 繪製 ====================

def update_effects():
    """統一更新所有特效"""
    update_explosions()

def draw_effects(surface, player_x, player_y):
    """統一繪製所有特效"""
    draw_muzzle_flash(surface, player_x, player_y)
    draw_explosions(surface)
