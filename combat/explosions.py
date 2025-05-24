# combat/explosions.py
import pygame
import math
from ui.ui import add_floating_text

# 存放所有正在發生的爆炸
active_explosions = []

class Explosion:
    """爆炸類別，造成範圍內敵人傷害"""
    def __init__(self, x, y, radius=50, damage=50, duration=500):
        self.x = x
        self.y = y
        self.radius = radius
        self.damage = damage
        self.duration = duration  # 持續時間（毫秒）
        self.start_time = pygame.time.get_ticks()
        self.exploded = False

    def explode(self):
        """對範圍內的敵人造成傷害"""
        if self.exploded:
            return
        self.exploded = True

        for enemy in enemies[:]:
            dist = math.hypot(enemy.x - self.x, enemy.y - self.y)
            if dist < self.radius:
                enemy.hp -= self.damage
                add_floating_text("💥 Explosion!", (enemy.x, enemy.y), 800)
                if enemy.hp <= 0:
                    enemies.remove(enemy)

    def update(self):
        """更新爆炸狀態，檢查是否該移除"""
        if pygame.time.get_ticks() - self.start_time > self.duration:
            return False  # 爆炸結束，應該被移除
        return True

    def draw(self, surface):
        """繪製爆炸效果"""
        if not self.exploded:
            pygame.draw.circle(surface, (255, 0, 0), (int(self.x), int(self.y)), 5)
        else:
            pygame.draw.circle(surface, (255, 165, 0), (int(self.x), int(self.y)), self.radius, 2)

def trigger_explosion(enemies, explosion_center, explosion_damage, explosion_radius): #  <<<===  新增 enemies 參數 (第一個參數)
    """觸發爆炸"""
    explosion = Explosion(x, y, radius, damage)
    explosion.explode()
    active_explosions.append(explosion)

def update_explosions():
    """更新並移除過期的爆炸"""
    for explosion in active_explosions[:]:
        if not explosion.update():
            active_explosions.remove(explosion)

def draw_explosions(surface):
    """繪製所有爆炸"""
    for explosion in active_explosions:
        explosion.draw(surface)
