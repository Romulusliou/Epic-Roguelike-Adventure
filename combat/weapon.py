# combat/weapon.py
import pygame
import math
import random
from combat.bullets import Bullet
from combat.explosions import Explosion
from ui.ui import add_floating_text

class Weapon:
    """武器基礎類別，所有武器都繼承這個類別"""
    def __init__(self, name):
        self.name = name

    def attack(self, player):
        """所有武器都需要實作 attack() 方法"""
        raise NotImplementedError("武器必須實作 attack() 方法")

class Sword(Weapon):
    """劍：近戰武器，揮動時造成範圍傷害"""
    def __init__(self):
        super().__init__("Sword")
        self.range = 80
        self.angle = math.radians(60)
        self.damage = 25
        self.swing_time = 300  # ms
        self.sword_hit_list = []
        self.sword_swinging = False
        self.sword_swing_start = 0

    def attack(self, player):
        if self.sword_swinging:
            return
        self.sword_swinging = True
        self.sword_swing_start = pygame.time.get_ticks()
        self.sword_hit_list = []

    def update_attack(self, player):
        """處理揮劍過程 & 計算範圍內敵人傷害"""
        if not self.sword_swinging:
            return

        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.sword_swing_start

        if elapsed > self.swing_time:
            self.sword_swinging = False
            return

        progress = elapsed / self.swing_time
        current_radius = progress * self.range
        current_sector_angle = progress * self.angle

        player_center = (player.x + player.size / 2, player.y + player.size / 2)

        for enemy in enemies[:]:
            if enemy in self.sword_hit_list:
                continue

            enemy_center = (enemy.x + enemy.size / 2, enemy.y + enemy.size / 2)
            dx = enemy_center[0] - player_center[0]
            dy = enemy_center[1] - player_center[1]
            distance = math.hypot(dx, dy)

            if distance > current_radius:
                continue

            angle_to_enemy = math.atan2(dy, dx)
            angle_difference = abs((angle_to_enemy - math.atan2(0, 1) + math.pi) % (2 * math.pi) - math.pi)

            if angle_difference <= current_sector_angle / 2:
                enemy.hp -= self.damage
                self.sword_hit_list.append(enemy)
                add_floating_text("⚔️ Sword Slash!", (enemy.x, enemy.y), 1000)
                
                if enemy.hp <= 0:
                    enemies.remove(enemy)

class Gun(Weapon):
    """槍：發射子彈"""
    def __init__(self):
        super().__init__("Gun")
        self.cooldown = 300  # ms
        self.last_shot_time = 0

    def attack(self, player):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time < self.cooldown:
            return  # 冷卻時間內不能開槍
        self.last_shot_time = current_time
        return Bullet(player.x, player.y, player.last_dir)

class Shotgun(Weapon):
    """霰彈槍：一次發射多顆子彈"""
    def __init__(self):
        super().__init__("Shotgun")
        self.cooldown = 500  # ms
        self.last_shot_time = 0
        self.spread = math.radians(30)  # 30度擴散角度
        self.bullet_count = 5  # 發射 5 顆子彈

    def attack(self, player):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time < self.cooldown:
            return
        self.last_shot_time = current_time

        bullets = []
        for i in range(self.bullet_count):
            offset = random.uniform(-self.spread / 2, self.spread / 2)
            angle = math.atan2(player.last_dir[1], player.last_dir[0]) + offset
            bullets.append(Bullet(player.x, player.y, (math.cos(angle), math.sin(angle))))
        return bullets

class Bomb(Weapon):
    """炸彈：爆炸造成範圍傷害"""
    def __init__(self):
        super().__init__("Bomb")
        self.cooldown = 1000  # ms
        self.last_throw_time = 0

    def attack(self, player):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_throw_time < self.cooldown:
            return
        self.last_throw_time = current_time
        return Explosion(player.x, player.y)

# 建立全局武器字典
WEAPONS = {
    "sword": Sword(),
    "gun": Gun(),
    "shotgun": Shotgun(),
    "bomb": Bomb(),
}
