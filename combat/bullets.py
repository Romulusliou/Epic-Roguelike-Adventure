# combat/bullets.py
import pygame
import math
from enemy.enemy import enemies
from ui.ui import add_floating_text
from combat.explosions import Explosion

# 存放所有活動中的子彈
active_bullets = []

class Bullet:
    """子彈類別，處理移動 & 碰撞"""
    def __init__(self, x, y, direction, speed=10, damage=10, explosive=False):
        self.x = x
        self.y = y
        self.vx = direction[0] * speed
        self.vy = direction[1] * speed
        self.damage = damage
        self.explosive = explosive  # 是否為爆炸性子彈
        self.radius = 5  # 子彈大小
        self.alive = True  # 是否還在飛行中

    def update(self):
        """更新子彈位置，檢查邊界 & 碰撞"""
        if not self.alive:
            return

        # 移動子彈
        self.x += self.vx
        self.y += self.vy

        # 超出畫面則移除
        if self.x < 0 or self.x > pygame.display.get_surface().get_width() or \
           self.y < 0 or self.y > pygame.display.get_surface().get_height():
            self.alive = False

        # 檢查碰撞
        for enemy in enemies:
            if self.check_collision(enemy):
                enemy.hp -= self.damage
                if self.explosive:
                    add_floating_text("💥 Explosion!", (enemy.x, enemy.y), 800)
                    explosion = Explosion(self.x, self.y)  # 產生爆炸
                    explosion.explode()
                if enemy.hp <= 0:
                    enemies.remove(enemy)
                self.alive = False
                break

    def check_collision(self, enemy):
        """檢查子彈是否擊中敵人"""
        enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.size, enemy.size)
        bullet_rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
        return enemy_rect.colliderect(bullet_rect)

    def draw(self, surface):
        """繪製子彈"""
        pygame.draw.circle(surface, (255, 165, 0), (int(self.x), int(self.y)), self.radius)

def shoot_bullet(x, y, direction):
    """創建並發射一顆普通子彈"""
    bullet = Bullet(x, y, direction)
    active_bullets.append(bullet)

def update_bullets():
    """更新 & 移除無效子彈"""
    for bullet in active_bullets[:]:
        bullet.update()
        if not bullet.alive:
            active_bullets.remove(bullet)

def draw_bullets(surface):
    """繪製所有子彈"""
    for bullet in active_bullets:
        bullet.draw(surface)
