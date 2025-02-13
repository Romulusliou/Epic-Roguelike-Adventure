# main.py
import pygame
import sys
import random
import math
import os
from settings import settings #  導入 settings 模組
import ui #  <<<===  導入 ui 模組


# ================= Global Variables =====================
player_hp = 100
player_max_hp = 100
player_level = 1
player_exp = 0
player_speed = 5
player_atk_cd = 200 # ms (攻擊冷卻)
player_last_attack_time = 0
player_equipment = [] #  玩家裝備列表，每個裝備是一個字典 {"name": str, "rare": bool}

enemies = []
bombs = []
current_wave = 1
max_waves = 3 #  <<<===  最大波數調整為 3 波
wave_interval = 5000 # ms (波與波之間的時間間隔)
last_wave_time = 0
wave_started = False #  標記是否已開始生成敵人
wave_enemy_count = 0 #  追蹤當前波次已生成的敵人數量
enemies_in_wave = 5 #  每波預設 5 個敵人
enemies_killed_in_wave = 0 #  追蹤當前波次已殺死的敵人數量
boss_wave_mod = 5 #  每隔 5 波生成 Boss

equipment_icons = {
    "Flame Sword": "🔥🗡️",
    "Explosive Shotgun": "💣🔫",
    "Guardian Shield": "🛡️",
    "Wind Boots": "💨👟",
    "Energy Core": "⚛️"
}

equipment_descriptions = {
    "Flame Sword": "+10 ATK",
    "Explosive Shotgun": "Splash DMG",
    "Guardian Shield": "+20 DEF",
    "Wind Boots": "+2 SPD",
    "Energy Core": "CD -10%"
}


# ================= Game States =====================
game_state = "menu" #  <<<===  遊戲初始狀態設定為 "menu"
user_input = "" # 儲存玩家輸入的文字
is_upgrading = False # 是否進入升級狀態
upgrade_done = False # 升級選項是否選擇完成


# ================= Global Effect Variables =====================
muzzle_flash_time = 0
muzzle_flash_duration = 100 # ms

screen_shake_time = 0
screen_shake_intensity = 0


# ================= Classes =====================
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.size = 50
        # 建立一個透明背景的 Surface
        self.original_image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        # 從 settings 中讀取顏色，假設 settings.CYAN 已定義
        pygame.draw.circle(self.original_image, settings.CYAN, (self.size // 2, self.size // 2), self.size // 2)
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()  # 確保 rect 被正確設定
