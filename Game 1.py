import pygame
import random
import sys
import math
import os
import keyboard #  <--- 導入 keyboard 函式庫
import sys, time, random, math

# It is expected that main.py (or equivalent) will call settings.init_settings()
# and pass the returned dictionary to the game logic.
# For now, we'll assume these variables will be provided by such a call.
# screen, WIDTH, HEIGHT, fonts, colors etc. will be obtained from the settings dict.

# Example placeholders (these would be set by the caller using settings)
screen = None # Will be set by settings['screen']
WIDTH, HEIGHT = 0, 0 # Will be set by settings['WIDTH'], settings['HEIGHT']
font = None # Will be set by settings['fonts']['main']
equip_font = None # Will be set by settings['fonts']['equip']
upgrade_font = None # Will be set by settings['fonts']['upgrade']
upgrade_font_small = None # Will be set by settings['fonts']['upgrade_small']
COLOR_DICT = {} # Will be set by settings['colors']
# Individual colors like BLACK, WHITE etc. will also be available from the settings dict.
BLACK, WHITE, GREEN, ORANGE, BLUE, YELLOW, CYAN, RED, PINK, BROWN = [(0,0,0)]*10 # Placeholders
LIGHT_GREEN, LIGHT_YELLOW, LIGHT_BLUE, LIGHT_CYAN, PURPLE, DARK_RED = [(0,0,0)]*6 # Placeholders


user_input = ""  # 儲存玩家輸入的文字

game_state = "playing"  # 可用值："playing"（遊戲中）、"paused"（暫停中）、"menu"（主選單）

for event in pygame.event.get():
    if event.type == pygame.QUIT:
        running = False

    elif event.type == pygame.KEYDOWN:
        print(f"[DEBUG] KEYDOWN: {event.key}")  # 顯示按鍵代碼

        if event.key == pygame.K_RETURN:  # 按 Enter 確認輸入
            print(f"[DEBUG] 玩家輸入完成: {user_input}")
            user_input = ""  # 清空輸入框

        elif event.key == pygame.K_BACKSPACE:  # 退格刪除字元
            user_input = user_input[:-1]
            print(f"[DEBUG] 玩家刪除字元，剩餘輸入: {user_input}")

        elif event.key == pygame.K_SPACE:  # 空白鍵
            user_input += " "  # 加入空格

        else:
            try:
                char = event.unicode  # 嘗試取得按鍵對應的文字
                print(f"[DEBUG] 玩家輸入: {char}")
                user_input += char
            except:
                print("[DEBUG] 無法解析此鍵")

    # 遊戲進行中
    if game_state == "playing":
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_state = "paused"  # 按下 ESC 進入暫停狀態
            # 其他遊戲進行中的按鍵處理...
    
    # 暫停狀態下，處理暫停選單事件
    elif game_state == "paused":
        if event.type == pygame.KEYDOWN:
            # 你可以讓 ESC 再次切換回遊戲，或者僅靠滑鼠點擊選單選項
            if event.key == pygame.K_ESCAPE:
                game_state = "playing"
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # 假設「回到首頁」選項在畫面中的某個區域，這裡用範例座標判斷
            if (WIDTH // 2 - 100 <= mouse_x <= WIDTH // 2 + 100) and (HEIGHT // 2 + 70 <= mouse_y <= HEIGHT // 2 + 130):
                game_state = "menu"  # 切換到主選單狀態
            # 也可以在這裡加入「繼續遊戲」和「設定」的點擊處理

    # 主選單狀態下，處理按鍵或滑鼠來選擇開始遊戲等功能
    elif game_state == "menu":
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                game_state = "playing"  # 按 Enter 開始遊戲（或重新開始）







# Color definitions are now loaded from settings.py

# ================= Floating Text System =====================
floating_texts = []  # Each: {"text": str, "pos": (x,y), "timer": ms}

def add_floating_text(text, pos, duration=1000):
    floating_texts.append({"text": text, "pos": pos, "timer": duration})

def update_floating_texts(dt):
    for obj in floating_texts[:]:
        obj["timer"] -= dt
        if obj["timer"] <= 0:
            floating_texts.remove(obj)

def draw_floating_texts(surface):
    for obj in floating_texts:
        txt = upgrade_font.render(obj["text"], True, BLACK)
        surface.blit(txt, obj["pos"])

# ================= Global Effect Variables =====================
muzzle_flash_time = 0
muzzle_flash_duration = 100  # ms

screen_shake_time = 0
screen_shake_intensity = 0

# ================= Player Parameters =====================
base_player_speed = 5
player_speed = base_player_speed
player_size = 40
player_x = WIDTH // 2
player_y = HEIGHT // 2
player_hp = 100
player_max_hp = 100
player_level = 1
player_exp = 0
player_hp_regen = 0      #  新增：生命回復速度
player_crit_rate = 0.0   #  新增：暴擊率 (0.0 ~ 1.0)
player_dodge_rate = 0.0  #  新增：閃避率 (0.0 ~ 1.0)


upgrade_options_data = [ #  <<<=== 將 upgrade_options_data 放在這裡 (或其他全局變數定義區)
    # ---------- 基礎素質升級 ----------
    {
        "type": "stat",
        "subtype": "hp",
        "name": "強化生命值",
        "description": "永久增加 20 點生命值上限，提升生存能力。",
        "effect": "player_max_hp += 20",
        "level_required": 1,
        "display_color": "GREEN", #  新增：選項框顏色
        "key_binding": "1",      #  新增：綁定按鍵 (預設使用數字鍵 1, 2, 3)
    },
    
    # ---------- 基礎素質升級 ----------
    {
        "type": "stat",
        "subtype": "hp",
        "name": "強化生命值",
        "description": "永久增加 20 點生命值上限，提升生存能力。",
        "effect": "player_max_hp += 20",
        "level_required": 1,
        "display_color": "GREEN", #  新增：選項框顏色
        "key_binding": "1",      #  新增：綁定按鍵 (預設使用數字鍵 1, 2, 3)
    },
    {
        "type": "stat",
        "subtype": "attack",
        "name": "強化攻擊力",
        "description": "永久增加 5 點基礎攻擊力，提升傷害輸出。",
        "effect": "attack_damage += 5",
        "level_required": 1,
        "display_color": "ORANGE", # 新增：選項框顏色
        "key_binding": "2",      # 新增：綁定按鍵
    },
    {
        "type": "stat",
        "subtype": "speed",
        "name": "強化移動速度",
        "description": "永久提升 10% 移動速度，更加靈活。", # 修改為百分比提升更直觀
        "effect": "player_speed *= 1.1", #  使用乘法提升百分比
        "level_required": 2,      #  移動速度提升可以設定等級 2 解鎖
        "display_color": "YELLOW", # 新增：選項框顏色
        "key_binding": "3",      # 新增：綁定按鍵
    },
    {
        "type": "stat",
        "subtype": "hp_regen",
        "name": "強化生命回復",
        "description": "永久提升 1 點/秒 生命回復速度，增強續戰力。",
        "effect": "player_hp_regen += 1",
        "level_required": 3,      # 生命回復可以設定等級 3 解鎖
        "display_color": "CYAN",   # 新增：選項框顏色
        "key_binding": "4",      # 新增：綁定按鍵 (後續選項使用數字鍵 4, 5, 6...)
    },
    {
        "type": "stat",
        "subtype": "crit_rate",
        "name": "強化暴擊率",
        "description": "永久提升 5% 暴擊率，造成更高爆發傷害。", # 修改為百分比提升更直觀
        "effect": "player_crit_rate += 0.05", #  使用浮點數表示百分比
        "level_required": 4,      # 暴擊率可以設定等級 4 解鎖
        "display_color": "RED",    # 新增：選項框顏色
        "key_binding": "5",      # 新增：綁定按鍵
    },
    {
        "type": "stat",
        "subtype": "dodge_rate",
        "name": "強化閃避率",
        "description": "永久提升 2% 閃避率，更不容易受到傷害。", # 修改為百分比提升更直觀
        "effect": "player_dodge_rate += 0.02", # 使用浮點數表示百分比
        "level_required": 5,      # 閃避率可以設定等級 5 解鎖
        "display_color": "PINK",   # 新增：選項框顏色
        "key_binding": "6",      # 新增：綁定按鍵
    },

    # ---------- 新增武器 ----------
    {
        "type": "bullet",
        "subtype": "gun",
        "name": "解鎖基礎槍",
        "description": "獲得基礎槍，遠程攻擊能力UP！",
        "effect": "weapons['bullet'] = True",
        "level_required": 1,
        "display_color": "BLUE",   # 新增：選項框顏色
        "key_binding": "7",      # 新增：綁定按鍵
    },
    #                  

    # ... 可以繼續擴充更多升級選項 ...
]




# ================= Equipment System =====================
player_equipment = []  # Each: {"name": str, "rare": bool}
equipment_icons = {
    "Flame Sword": "🔥",
    "Explosive Shotgun": "💥",
    "Guardian Shield": "🛡",
    "Wind Boots": "🌪",
    "Energy Core": "⚡"
}
equipment_descriptions = {
    "Flame Sword": "Sword attacks inflict burning (3s, 5 dmg/sec).",
    "Explosive Shotgun": "Bullets cause explosions with splash damage.",
    "Guardian Shield": "50% chance to block damage (half damage).",
    "Wind Boots": "Increase speed by 15% and 10% chance to dodge attacks.",
    "Energy Core": "Triggers electric shock every 10s (50 dmg) to nearby enemies."
}

# ================= Weapon System =====================
weapons = {"sword": True, "bullet": False}
sword_advanced = False

# --- Sword Parameters ---
attack_damage = 25
sword_swinging = False
sword_swing_start = 0
sword_duration = 300  # ms
sword_range = 80      # Final attack radius
sword_fan_angle = math.radians(60)  # Final sector angle (60°)
sword_hit_list = []
刀_範圍 = sword_range #  範例: 使用 刀_範圍 變數控制刀的範圍 (請根據您的實際程式碼調整變數名稱)
刀_攻擊速度 = 1      #  範例: 使用 刀_攻擊速度 控制刀的攻擊速度 (數值越大速度越慢，數值越小速度越快，預設值為 1)

# --- Bullet Parameters (Gun) ---
bullets = []  # Each bullet: {"x", "y", "dir": (dx,dy)}
bullet_cooldown = 300  # ms
last_bullet_time = 0
bullet_speed = 10
bullet_count = 3  # Number of bullets fired at once
bullet_spread = math.radians(30)  # Spread angle of 30°
last_dir = (0, -1)
槍_子彈數量 = bullet_count # 範例: 使用 槍_子彈數量 變數控制子彈數量
槍_射擊間隔 = bullet_cooldown / 1000 # 範例: 使用 槍_射擊間隔 控制射速 (單位: 秒) (預設值為 bullet_cooldown/1000)

def melee_attack():
    """執行近戰攻擊（劍），檢測範圍內的敵人並造成傷害。"""
    global enemies
    sword_range = 50  # 劍攻擊範圍
    for enemy in enemies:
        if math.hypot(enemy.x - player_x, enemy.y - player_y) < sword_range:
            enemy.hp -= 25  # 劍的傷害
            enemy.burn_time = 3000  # 點燃敵人 3 秒
            enemy.last_burn_tick = pygame.time.get_ticks()
            add_floating_text("⚔️ Sword Slash!", (enemy.x, enemy.y), 1000)  # 顯示攻擊特效



def ranged_attack():
    """執行遠程攻擊（子彈），生成新的子彈並追蹤敵人。"""
    global bullets
    bullet_speed = 8
    bullet_damage = 10
    bullets.append({"x": player_x, "y": player_y, "vx": bullet_speed, "vy": 0, "damage": bullet_damage})


def handle_attacks():
    """統一處理攻擊，根據輸入決定近戰或遠程攻擊。"""
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:  # 近戰攻擊（按空格鍵）
        melee_attack()
    if keys[pygame.K_SPACE]:  # 遠程攻擊（按 F 鍵）
        ranged_attack()

# ================= upgrade system =====================
def draw_upgrade_overlay(frame_surface, upgrade_options, player_level): # 修改: 接收 upgrade_options 和 player_level
    # In a real scenario, WIDTH and HEIGHT would be initialized from settings
    if WIDTH == 0 or HEIGHT == 0: # Basic check if settings were loaded
        print("Error: WIDTH or HEIGHT not initialized. Ensure settings are loaded.")
        return # Avoid pygame.Surface error if WIDTH/HEIGHT are zero

    # 在已有戰鬥畫面上疊加半透明濾鏡
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((255, 255, 255, 0)) # Assuming WHITE is available or use (255,255,255,0)
    frame_surface.blit(overlay, (0, 0))

    box_width, box_height = 300, 200
    spacing = 50
    total_width = len(upgrade_options) * box_width + (len(upgrade_options) - 1) * spacing # 修改: 根據選項數量計算總寬度
    start_x = (WIDTH - total_width) // 2
    start_y = (HEIGHT - box_height) // 2

    for i, option in enumerate(upgrade_options): # 修改: 迴圈處理升級選項
        box_x = start_x + i * (box_width + spacing)
        box_rect = pygame.Rect(box_x, start_y, box_width, box_height)
        # Ensure BLACK, COLOR_DICT, GREEN, upgrade_font, upgrade_font_small are loaded from settings
        if not all([COLOR_DICT, upgrade_font, upgrade_font_small]):
            print("Error: Colors or fonts not initialized in draw_upgrade_overlay.")
            return

        pygame.draw.rect(frame_surface, COLOR_DICT.get("BLACK", (0,0,0)), box_rect, 2)

        # 根據 upgrade_options_data 中的 display_color 決定方框顏色
        box_color_name = option.get("display_color", "GREEN") # 預設顏色為 GREEN
        box_color = COLOR_DICT.get(box_color_name, COLOR_DICT.get("GREEN",(0,255,0))) # 使用 COLOR_DICT 取得顏色值，預設為 GREEN
        pygame.draw.rect(frame_surface, box_color, (box_rect.x + 20, box_rect.y + 20, box_width - 40, box_height - 80))

        txt_option_name = upgrade_font.render(option["name"], True, COLOR_DICT.get("BLACK",(0,0,0))) # 使用選項名稱
        frame_surface.blit(txt_option_name, (box_rect.x + 20, box_rect.y + box_height - 100)) # 調整位置

        txt_description = upgrade_font_small.render(option["description"], True, COLOR_DICT.get("BLACK",(0,0,0))) # 使用選項描述
        frame_surface.blit(txt_description, (box_rect.x + 20, box_rect.y + box_height - 60)) # 調整位置

        # 顯示按鍵提示 (例如 "Press 1", "Press 2", "Press Q" etc.)，使用 key_binding 屬性
        key_prompt_text = f"Press {option['key_binding']}"
        key_prompt = upgrade_font.render(key_prompt_text, True, COLOR_DICT.get("BLACK",(0,0,0)))
        frame_surface.blit(key_prompt, (box_rect.x + 20, box_rect.y + box_height - 30)) # 調整位置


    prompt = upgrade_font.render("Choose upgrade", True, COLOR_DICT.get("BLACK",(0,0,0))) # 提示文字簡化
    frame_surface.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, start_y + box_height + 20))
    
    if screen: # Ensure screen is initialized
        screen.blit(frame_surface, (0, 0))
        pygame.display.update()

class Bomb:
    def __init__(self, x, y, target_x, target_y):
        self.x = x
        self.y = y
        self.target_x = target_x
        self.target_y = target_y
        self.speed = 5  
        self.exploded = False
        self.explosion_radius = 50  
        self.damage = 50  
    
    def move(self):
        if not self.exploded:
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            dist = math.hypot(dx, dy)
            if dist > 0:
                self.x += (dx / dist) * self.speed
                self.y += (dy / dist) * self.speed

            if dist < 5:
                self.explode()

    def explode(self):
        self.exploded = True
        for enemy in enemies:  
            if math.hypot(enemy.x - self.x, enemy.y - self.y) < self.explosion_radius:
                enemy.hp -= self.damage

    def draw(self, surface):
        if not self.exploded:
            pygame.draw.circle(surface, (255, 0, 0), (int(self.x), int(self.y)), 5)
        else:
            pygame.draw.circle(surface, (255, 255, 0), (int(self.x), int(self.y)), self.explosion_radius, 2)

    def should_be_removed(self): #  <<<===  新增 should_be_removed(self) 方法
        # 判斷炸彈是否應該被移除的邏輯
        if self.exploded: #  如果炸彈已經爆炸 (self.exploded 為 True)
            return True #  返回 True，表示應該被移除
        else: #  否則 (炸彈還沒爆炸)
            return False #  返回 False，表示不應該被移除


# === Begin Enemy Management Module ===
ENEMY_STATS = {
    "normal": {"speed": 2, "size": 20, "color": RED, "max_hp": 100},
    "elite": {"speed": 3, "size": 20, "color": PURPLE, "max_hp": 150},
    "swift": {"speed": 4, "size": 18, "color": (0, 200, 200), "max_hp": 80},
    "tank": {"speed": 1, "size": 30, "color": (100, 100, 100), "max_hp": 200},
    "healer": {"speed": 2, "size": 22, "color": (0, 255, 255), "max_hp": 120},
    "bomber": {"speed": 2, "size": 24, "color": (255, 165, 0), "max_hp": 100},
    "summoner": {"speed": 1.5, "size": 26, "color": (255, 0, 255), "max_hp": 130},
    "boss": {"speed": 1, "size": 40, "color": DARK_RED, "max_hp": 500}
}


class Enemy:
    def __init__(self, x, y, etype, wave):
        self.x = x
        self.y = y
        self.etype = etype
        self.set_attributes(etype, wave)
        self.burn_time = 0
        self.last_burn_tick = 0
        self.attack_cooldown = 0  # 攻擊冷卻時間
        self.summon_cooldown = 0  # 召喚冷卻
        self.shield = 0  # 坦克用護盾
        self.direction = random.choice([-1, 1])  # swift Z 字形移動

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

    def update_behavior(self, target_x, target_y, enemies):
        """根據敵人類型執行不同的行為"""
        if self.etype == "normal":
            self.move_towards(target_x, target_y)

        elif self.etype == "elite":
            self.move_towards(target_x, target_y)
            if self.attack_cooldown <= 0:  # 觸發短暫衝刺
                self.speed *= 2
                self.attack_cooldown = 60  # 1 秒後才能再衝刺

        elif self.etype == "swift":
            self.x += self.direction * self.speed  # Z 字形移動
            if random.random() < 0.02:  # 偶爾改變方向
                self.direction *= -1
            if self.attack_cooldown <= 0 and self.is_near(target_x, target_y, 50):
                self.speed *= 3  # 瞬間加速
                self.attack_cooldown = 80

        elif self.etype == "tank":
            self.move_towards(target_x, target_y)
            if pygame.time.get_ticks() % 5000 < 100:  # 每 5 秒獲得護盾
                self.shield = 1

        elif self.etype == "healer":
            self.x += random.uniform(-1, 1) * self.speed  # 避免站在原地
            self.y += random.uniform(-1, 1) * self.speed
            self.heal_allies(enemies)

        elif self.etype == "bomber":
            if self.attack_cooldown <= 0:
                self.throw_bomb(target_x, target_y)
                self.attack_cooldown = 120  # 投擲冷卻時間

        elif self.etype == "summoner":
            if self.summon_cooldown <= 0:
                self.summon_enemy()
                self.summon_cooldown = 200
            if self.hp < self.max_hp * 0.5:
                self.x += (self.x - target_x) * 0.1  # 逃跑

        elif self.etype == "boss":
            if random.random() < 0.5:
                self.throw_bomb(target_x, target_y)
            if random.random() < 0.3:
                self.summon_enemy()
            if random.random() < 0.2:
                self.speed *= 2  # 偶爾衝刺

    def apply_burn(self, current_time):
        if self.burn_time > 0 and current_time - self.last_burn_tick >= 1000:
            self.hp -= 5
            self.burn_time -= 1000
            self.last_burn_tick = current_time

    def draw(self, surface):
        rect = pygame.Rect(self.x, self.y, self.size, self.size)
        # Ensure BLACK, GREEN are loaded from settings
        current_black = COLOR_DICT.get("BLACK", (0,0,0))
        current_green = COLOR_DICT.get("GREEN", (0,255,0))

        pygame.draw.rect(surface, self.color, rect)
        pygame.draw.rect(surface, current_black, (self.x, self.y - 10, self.size, 5))
        hp_bar = self.size * (self.hp / self.max_hp) if self.max_hp else 0
        pygame.draw.rect(surface, current_green, (self.x, self.y - 10, hp_bar, 5))

    def is_near(self, target_x, target_y, radius):
        return math.sqrt((self.x - target_x) ** 2 + (self.y - target_y) ** 2) < radius

    def throw_bomb(self, target_x, target_y):
        """炸彈客與 Boss 投擲爆炸物"""
        bomb = Bomb(self.x, self.y, target_x, target_y)
        bombs.append(bomb)

    def summon_enemy(self):
        """召喚師與 Boss 召喚小怪"""
        new_enemy = Enemy(self.x + random.randint(-30, 30), self.y + random.randint(-30, 30), "normal", 1)
        enemies.append(new_enemy)

    def heal_allies(self, enemies):
        """治療者治療附近敵人"""
        for enemy in enemies:
            if enemy != self and self.is_near(enemy.x, enemy.y, 100):
                enemy.hp = min(enemy.max_hp, enemy.hp + 10)
# === End Enemy Management Module ===

# ================= Enemy Parameters =====================
total_enemies_in_wave = 20
remaining_enemies_to_spawn = total_enemies_in_wave
max_enemies_on_screen = 10
current_wave = 1
max_waves = 10
enemies = []  # 存放 Enemy 物件

bombs = [] # 存放敵人投擲的炸彈



# 新增敵人類型對應字典，放在 spawn_enemy() 前面
wave_enemy_types = {
    1: ["normal"],
    3: ["normal", "elite", "swift"],
    5: ["normal", "elite", "swift", "tank"],
    7: ["normal", "elite", "swift", "tank", "healer"],
    9: ["normal", "elite", "swift", "tank", "healer", "bomber", "summoner"]
}

def spawn_enemy(wave):
    # 根據當前波數從字典中取得敵人類型列表，若沒有直接對應則取最大不超過的鍵
    types = wave_enemy_types.get(wave)
    if types is None:
        keys = sorted(wave_enemy_types.keys())
        for k in reversed(keys):
            if wave >= k:
                types = wave_enemy_types[k]
                break
    # 隻在第一關時，types 應為 ["normal"]
    etype = random.choice(types)
    # 如果是最終波且還沒有boss，則設定為boss
    if wave == max_waves and not any(enemy.etype == "boss" for enemy in enemies):
        etype = "boss"
    x = random.randint(0, WIDTH - 100)
    y = random.randint(0, HEIGHT - 100)
    return Enemy(x, y, etype, wave)


# ================= Energy Core Timer =====================
last_elec_time = 0

# ================= Drop Equipment Function =====================
def drop_equipment(enemy):
    global player_equipment
    def add_eq(eq_name, rare):
        if not any(e["name"] == eq_name for e in player_equipment):
            player_equipment.append({"name": eq_name, "rare": rare})
    if enemy.etype in ["normal", "elite"]:
        if random.random() < 0.1:
            eq = random.choice(["Flame Sword", "Explosive Shotgun", "Guardian Shield", "Wind Boots", "Energy Core"])
            add_eq(eq, False)
    elif enemy.etype == "boss":
        rare = random.random() < 0.5
        eq = random.choice(["Flame Sword", "Explosive Shotgun", "Guardian Shield", "Wind Boots", "Energy Core"])
        add_eq(eq, rare)

# ================= Miscellaneous =====================
player_damage_cooldown = 500  # ms
last_damage_time = 0
clock = pygame.time.Clock()

def get_nearest_enemy(player_center):
    nearest_index = None
    enemy_center = None
    min_distance = float("inf")
    for i, enemy in enumerate(enemies):
        ex = enemy.x
        ey = enemy.y
        center = (ex + enemy.size/2, ey + enemy.size/2)
        dist = math.hypot(center[0]-player_center[0], center[1]-player_center[1])
        if dist < min_distance:
            min_distance = dist
            nearest_index = i
            enemy_center = center
    return nearest_index, enemy_center

def start_screen():
    # Ensure WIDTH, HEIGHT, WHITE, font, BLACK, screen are loaded
    if not all([WIDTH, HEIGHT, font, screen]):
        print("Error: Essential settings not loaded for start_screen.")
        # Potentially exit or handle error, for now, just return to avoid crashing
        pygame.quit()
        sys.exit()
        return

    current_white = COLOR_DICT.get("WHITE", (255,255,255))
    current_black = COLOR_DICT.get("BLACK", (0,0,0))

    waiting = True
    while waiting:
        frame = pygame.Surface((WIDTH, HEIGHT))
        frame.fill(current_white)
        title_text = font.render("穿越成為成最強冒險家", True, current_black)
        prompt_text = font.render("Press ENTER to Start", True, current_black)
        frame.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//2 - title_text.get_height() - 20))
        frame.blit(prompt_text, (WIDTH//2 - prompt_text.get_width()//2, HEIGHT//2 + 20))
        screen.blit(frame, (0, 0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False

def end_screen():
    # Ensure WIDTH, HEIGHT, WHITE, font, RED, upgrade_font, BLACK, screen are loaded
    if not all([WIDTH, HEIGHT, font, upgrade_font, screen, COLOR_DICT]):
        print("Error: Essential settings not loaded for end_screen.")
        pygame.quit()
        sys.exit()
        return False # Default to quit if settings are missing

    current_white = COLOR_DICT.get("WHITE", (255,255,255))
    current_red = COLOR_DICT.get("RED", (255,0,0))
    current_black = COLOR_DICT.get("BLACK", (0,0,0))

    waiting = True
    while waiting:
        frame = pygame.Surface((WIDTH, HEIGHT))
        frame.fill(current_white)
        prompt_text = font.render("Game Over", True, current_red)
        option_text = upgrade_font.render("Press R to Restart or Q to Quit", True, current_black)
        frame.blit(prompt_text, (WIDTH//2 - prompt_text.get_width()//2, HEIGHT//2 - prompt_text.get_height()))
        frame.blit(option_text, (WIDTH//2 - option_text.get_width()//2, HEIGHT//2 + 20))
        screen.blit(frame, (0, 0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                elif event.key == pygame.K_q:
                    return False
                
def draw_hp_bar(surface, player_hp, player_max_hp):
    """繪製血條"""
    # Ensure BLACK, GREEN, font, WIDTH are loaded
    if not all ([font, COLOR_DICT, WIDTH]):
        print("Error: settings not loaded for draw_hp_bar")
        return
    current_black = COLOR_DICT.get("BLACK", (0,0,0))
    current_green = COLOR_DICT.get("GREEN", (0,255,0))

    hp_bar_width = 200
    hp_ratio = player_hp / player_max_hp
    pygame.draw.rect(surface, current_black, (WIDTH - hp_bar_width - 20, 20, hp_bar_width, 20))
    pygame.draw.rect(surface, current_green, (WIDTH - hp_bar_width - 20, 20, hp_bar_width * hp_ratio, 20))
    hp_text = font.render(f"HP: {player_hp}/{player_max_hp}", True, current_black)
    surface.blit(hp_text, (WIDTH - hp_bar_width - 20, 50))

def draw_exp_bar(surface, player_exp, player_level):
    """繪製經驗條"""
    # Ensure BLACK, GREEN are loaded
    if not COLOR_DICT:
        print("Error: settings not loaded for draw_exp_bar")
        return
    current_black = COLOR_DICT.get("BLACK", (0,0,0))
    current_green = COLOR_DICT.get("GREEN", (0,255,0))

    exp_bar_width = 200
    required_exp = 30 * (player_level ** 2)
    exp_ratio = player_exp / required_exp
    pygame.draw.rect(surface, current_black, (20, 20, exp_bar_width, 10))
    pygame.draw.rect(surface, current_green, (20, 20, exp_bar_width * exp_ratio, 10))

def draw_game_info(surface, player_level, current_wave, max_waves):
    """顯示遊戲基本資訊"""
    # Ensure font, BLACK are loaded
    if not all([font, COLOR_DICT]):
        print("Error: settings not loaded for draw_game_info")
        return
    current_black = COLOR_DICT.get("BLACK", (0,0,0))
    level_text = font.render(f"Level: {player_level}", True, current_black)
    surface.blit(level_text, (20, 40))
    wave_text = font.render(f"Wave: {current_wave}/{max_waves}", True, current_black)
    surface.blit(wave_text, (20, 100))

def draw_equipment_panel(surface, player_equipment, equipment_icons, equipment_descriptions):
    """繪製裝備欄"""
    # Ensure WIDTH, BLACK, equip_font, upgrade_font are loaded
    if not all([WIDTH, COLOR_DICT, equip_font, upgrade_font]):
        print("Error: settings not loaded for draw_equipment_panel")
        return
    current_black = COLOR_DICT.get("BLACK", (0,0,0))
    panel_x = WIDTH - 300
    panel_y = 150
    panel_width = 280
    panel_height = 300
    pygame.draw.rect(surface, current_black, (panel_x, panel_y, panel_width, panel_height), 2)
    for i, eq in enumerate(player_equipment):
        icon = equipment_icons.get(eq["name"], eq["name"])
        if eq["rare"]:
            icon += "★"
        txt_icon = equip_font.render(icon, True, current_black)
        txt_desc = upgrade_font.render(equipment_descriptions.get(eq["name"], ""), True, current_black)
        surface.blit(txt_icon, (panel_x + 10, panel_y + 10 + i * 50))
        surface.blit(txt_desc, (panel_x + 50, panel_y + 10 + i * 50))

def draw_pause_menu(current_screen): # Renamed screen to current_screen to avoid conflict with global
    """繪製暫停選單"""
    # Ensure WIDTH, HEIGHT, font (from settings['fonts']['main']) are loaded
    # The original code uses `font_path` to load a new font instance here.
    # It's better to use one of the pre-loaded fonts from settings.
    # Assuming `settings['fonts']['main']` is desired here, or a specific large font.
    if not all([WIDTH, HEIGHT, font, current_screen]): # font here refers to global placeholder
        print("Error: settings not loaded for draw_pause_menu")
        return

    # Use a pre-loaded font, e.g., the main font, or a specific menu font if defined in settings
    menu_font = pygame.font.Font(None, 50) # Fallback, ideally use settings['fonts']['menu_large']
    if 'main' in fonts: # fonts is the dict from settings
        try:
            # Attempt to create a larger version of the main font if path is stored, or use a specific menu font
            # For simplicity, let's assume main_font can be resized or a dedicated menu font is used.
            # This example will just use a new system font if font_path is not easily accessible
             menu_font = pygame.font.Font(fonts['main'].name, 50) if fonts['main'].name else pygame.font.SysFont("arial", 50)
        except: # Fallback if name is not available or path is complex
            menu_font = pygame.font.SysFont("arial", 50)


    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))  # 半透明黑色背景
    current_screen.blit(overlay, (0, 0))

    options = ["繼續遊戲", "設定", "回到首頁"]
    option_y = HEIGHT // 2 - 50

    for option in options:
        text_surface = font.render(option, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(WIDTH // 2, option_y))
        screen.blit(text_surface, text_rect)
        option_y += 60

def draw_main_menu(screen):
    # Ensure WIDTH, HEIGHT, upgrade_font, screen are loaded
    if not all([WIDTH, HEIGHT, upgrade_font, screen]):
        print("Error: settings not loaded for draw_main_menu")
        return

    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((50, 50, 50, 255)) # Using direct color values
    # Assuming WHITE is (255,255,255)
    current_white_color = COLOR_DICT.get("WHITE", (255,255,255))
    title = upgrade_font.render("主選單", True, current_white_color)
    overlay.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 100))
    option = upgrade_font.render("按 Enter 開始遊戲", True, current_white_color)
    overlay.blit(option, (WIDTH // 2 - option.get_width() // 2, HEIGHT // 2))
    screen.blit(overlay, (0, 0))
    pygame.display.flip()




# is_upgrading and upgrade_done are now local to run_game in game.py
# The start_screen() call is now managed by run_game in game.py
# The main game loop is moved to run_game in game.py
# Pygame final quit and display updates are also in run_game.

# The global variables for game state like player_hp, enemies, current_wave, etc.,
# are removed from here as they will be local to the run_game function.
# Helper functions and class definitions remain for now.
# The placeholder settings variables (screen, WIDTH, HEIGHT, fonts, COLOR_DICT)
# also remain for now as the helper functions in this file still depend on them.
# In future refactoring, these functions will be moved to appropriate modules
# and will receive necessary data (like screen, settings) as parameters.