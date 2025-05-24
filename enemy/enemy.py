# enemy/enemy.py
import pygame
import math
import random
from ui.ui import add_floating_text
from combat.explosions import trigger_explosion
from game.game_state import enemies  # ✅ 確保 `enemy.py` 內部使用的是 `game_state.py` 的敵人列表


# 🦠 敵人類型設定
ENEMY_STATS = {
    "normal": {"speed": 2, "size": 20, "color": (255, 0, 0), "max_hp": 100},
    "elite": {"speed": 3, "size": 20, "color": (128, 0, 128), "max_hp": 150},
    "swift": {"speed": 4, "size": 18, "color": (0, 200, 200), "max_hp": 80},
    "tank": {"speed": 1, "size": 30, "color": (100, 100, 100), "max_hp": 200},
    "healer": {"speed": 2, "size": 22, "color": (0, 255, 255), "max_hp": 120},
    "bomber": {"speed": 2, "size": 24, "color": (255, 165, 0), "max_hp": 100},
    "summoner": {"speed": 1.5, "size": 26, "color": (255, 0, 255), "max_hp": 130},
    "boss": {"speed": 1, "size": 40, "color": (139, 0, 0), "max_hp": 500}
}



class Enemy:
    """敵人類別，負責移動 & 攻擊玩家"""
    def __init__(self, x, y, etype, wave):
        self.x = x
        self.y = y
        self.etype = etype
        self.set_attributes(etype, wave)
        self.attack_cooldown = 0
        self.summon_cooldown = 0
        self.shield = 0
        self.direction = random.choice([-1, 1])

    def set_attributes(self, etype, wave):
        stats = ENEMY_STATS[etype]
        self.speed = stats["speed"] * (0.5 if wave == 1 else 1 + (wave - 1) * 0.1)
        self.size = stats["size"]
        self.color = stats["color"]
        self.hp = self.max_hp = stats["max_hp"]

    def move_towards(self, target_x, target_y):
        """基礎移動方式：直線朝向玩家"""
        if target_x > self.x:
            self.x += self.speed
        elif target_x < self.x:
            self.x -= self.speed
        if target_y > self.y:
            self.y += self.speed
        elif target_y < self.y:
            self.y -= self.speed

    def update_behavior(self, player):
        """敵人 AI 行為模式"""
        if self.etype == "normal":
            self.move_towards(player.x, player.y)

        elif self.etype == "elite":
            self.move_towards(player.x, player.y)
            if self.attack_cooldown <= 0:
                self.speed *= 2
                self.attack_cooldown = 60

        elif self.etype == "swift":
            self.x += self.direction * self.speed
            if random.random() < 0.02:
                self.direction *= -1

        elif self.etype == "tank":
            self.move_towards(player.x, player.y)
            if pygame.time.get_ticks() % 5000 < 100:
                self.shield = 1

        elif self.etype == "healer":
            self.heal_allies()

        elif self.etype == "bomber":
            if self.attack_cooldown <= 0:
                trigger_explosion(self.x, self.y, 50, 50)
                self.attack_cooldown = 120

        elif self.etype == "summoner":
            if self.summon_cooldown <= 0:
                enemies.append(Enemy(self.x + 30, self.y + 30, "normal", 1))
                self.summon_cooldown = 200

        elif self.etype == "boss":
            if random.random() < 0.5:
                trigger_explosion(self.x, self.y, 70, 80)
            if random.random() < 0.3:
                enemies.append(Enemy(self.x + 50, self.y + 50, "normal", 1))
            if random.random() < 0.2:
                self.speed *= 2

    def heal_allies(self):
        """治療範圍內的敵人"""
        for enemy in enemies:
            if enemy != self and math.hypot(enemy.x - self.x, enemy.y - self.y) < 100:
                enemy.hp = min(enemy.max_hp, enemy.hp + 10)

    def draw(self, surface):
        """繪製敵人 & 血條"""
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.size, self.size))
        pygame.draw.rect(surface, (0, 0, 0), (self.x, self.y - 10, self.size, 5))
        hp_bar_width = self.size * (self.hp / self.max_hp)
        pygame.draw.rect(surface, (0, 255, 0), (self.x, self.y - 10, hp_bar_width, 5))

def update_enemies(player):
    """更新所有敵人"""
    for enemy in enemies[:]:
        enemy.update_behavior(player)
        if enemy.hp <= 0:
            enemies.remove(enemy)

def draw_enemies(surface):
    """繪製所有敵人"""
    for enemy in enemies:
        enemy.draw(surface)
