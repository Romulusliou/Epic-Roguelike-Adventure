import pygame
import random
import sys
import math
import os
import keyboard #  <--- 導入 keyboard 函式庫
import sys, time, random, math

# ================= Initialization =====================

pygame.init()

# ✅ 自適應螢幕解析度（自動適應全螢幕）
infoObject = pygame.display.Info()
WIDTH, HEIGHT = infoObject.current_w, infoObject.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("穿越成為成最強冒險家")

# ✅ 確保使用中文字型
# 🔥 自動切換到遊戲的實際目錄
os.chdir(os.path.dirname(os.path.abspath(__file__)))
font_path = os.path.join("fonts", "NotoSansTC-VariableFont_wght.ttf")  # 使用普通版字型
try:
    font = pygame.font.Font(font_path, 40)
except Exception as e:
    print(f"❌ 字型載入失敗: {e}")
    try:
        font = pygame.font.Font("msjh.ttc", 40)  # 微軟正黑體
    except Exception as e:
        print(f"❌ 微軟正黑體載入失敗: {e}")
        font = pygame.font.SysFont("arial", 40)  # 備用

# ✅ Emoji 字型處理（避免顯示錯誤）
try:
    equip_font = pygame.font.Font("seguiemj.ttf", 30)  # 支援 Emoji 的字型
except:
    print("Warning: Emoji font not found. Emoji may not display correctly.")
    equip_font = pygame.font.SysFont("arial", 30)

# 顯示升級選單的字型
upgrade_font = pygame.font.Font(font_path, 30) #  <<<===  修改: 使用 font_path 變數載入字型檔案
upgrade_font_small = pygame.font.Font(font_path, 24) #  <<<===  修改: 使用 font_path 變數載入字型檔案


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







# ==================== 顏色定義 ====================
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
RED = (255, 0, 0)
PINK = (255, 192, 203)
BROWN = (139, 69, 19)
LIGHT_GREEN = (144, 238, 144)
LIGHT_YELLOW = (255, 255, 224)
LIGHT_BLUE = (173, 216, 230)
LIGHT_CYAN = (224, 255, 255)
PURPLE = (128, 0, 128)
DARK_RED = (139, 0, 0)


COLOR_DICT = { #  定義 COLOR_DICT 字典 (請放在顏色常數定義 *下方*)
    "BLACK": BLACK,
    "GREEN": GREEN,
    "ORANGE": ORANGE,
    "BLUE": BLUE,
    "YELLOW": YELLOW,
    "CYAN": CYAN,
    "RED": RED,
    "PINK": PINK,
    "BROWN": BROWN,
    "LIGHT_GREEN": LIGHT_GREEN,
    "LIGHT_YELLOW": LIGHT_YELLOW,
    "LIGHT_BLUE": LIGHT_BLUE,
    "LIGHT_CYAN": LIGHT_CYAN,
    # ... 可以根據需要繼續擴充 ...
}

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
    # 在已有戰鬥畫面上疊加半透明濾鏡
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((255, 255, 255, 0))
    frame_surface.blit(overlay, (0, 0))

    box_width, box_height = 300, 200
    spacing = 50
    total_width = len(upgrade_options) * box_width + (len(upgrade_options) - 1) * spacing # 修改: 根據選項數量計算總寬度
    start_x = (WIDTH - total_width) // 2
    start_y = (HEIGHT - box_height) // 2

    for i, option in enumerate(upgrade_options): # 修改: 迴圈處理升級選項
        box_x = start_x + i * (box_width + spacing)
        box_rect = pygame.Rect(box_x, start_y, box_width, box_height)
        pygame.draw.rect(frame_surface, BLACK, box_rect, 2)

        # 根據 upgrade_options_data 中的 display_color 決定方框顏色
        box_color_name = option.get("display_color", "GREEN") # 預設顏色為 GREEN
        box_color = COLOR_DICT.get(box_color_name, GREEN) # 使用 COLOR_DICT 取得顏色值，預設為 GREEN
        pygame.draw.rect(frame_surface, box_color, (box_rect.x + 20, box_rect.y + 20, box_width - 40, box_height - 80))

        txt_option_name = upgrade_font.render(option["name"], True, BLACK) # 使用選項名稱
        frame_surface.blit(txt_option_name, (box_rect.x + 20, box_rect.y + box_height - 100)) # 調整位置

        txt_description = upgrade_font_small.render(option["description"], True, BLACK) # 使用選項描述
        frame_surface.blit(txt_description, (box_rect.x + 20, box_rect.y + box_height - 60)) # 調整位置

        # 顯示按鍵提示 (例如 "Press 1", "Press 2", "Press Q" etc.)，使用 key_binding 屬性
        key_prompt_text = f"Press {option['key_binding']}"
        key_prompt = upgrade_font.render(key_prompt_text, True, BLACK)
        frame_surface.blit(key_prompt, (box_rect.x + 20, box_rect.y + box_height - 30)) # 調整位置


    prompt = upgrade_font.render("Choose upgrade", True, BLACK) # 提示文字簡化
    frame_surface.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, start_y + box_height + 20))
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
        pygame.draw.rect(surface, self.color, rect)
        pygame.draw.rect(surface, BLACK, (self.x, self.y - 10, self.size, 5))
        hp_bar = self.size * (self.hp / self.max_hp) if self.max_hp else 0
        pygame.draw.rect(surface, GREEN, (self.x, self.y - 10, hp_bar, 5))

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
    waiting = True
    while waiting:
        frame = pygame.Surface((WIDTH, HEIGHT))
        frame.fill(WHITE)
        title_text = font.render("穿越成為成最強冒險家", True, BLACK)
        prompt_text = font.render("Press ENTER to Start", True, BLACK)
        frame.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//2 - title_text.get_height() - 20))
        frame.blit(prompt_text, (WIDTH//2 - prompt_text.get_width()//2, HEIGHT//2 + 20))
        screen.blit(frame, (0, 0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False

def end_screen():
    waiting = True
    while waiting:
        frame = pygame.Surface((WIDTH, HEIGHT))
        frame.fill(WHITE)
        prompt_text = font.render("Game Over", True, RED)
        option_text = upgrade_font.render("Press R to Restart or Q to Quit", True, BLACK)
        frame.blit(prompt_text, (WIDTH//2 - prompt_text.get_width()//2, HEIGHT//2 - prompt_text.get_height()))
        frame.blit(option_text, (WIDTH//2 - option_text.get_width()//2, HEIGHT//2 + 20))
        screen.blit(frame, (0, 0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                elif event.key == pygame.K_q:
                    return False
                
def draw_hp_bar(surface, player_hp, player_max_hp):
    """繪製血條"""
    hp_bar_width = 200
    hp_ratio = player_hp / player_max_hp
    pygame.draw.rect(surface, BLACK, (WIDTH - hp_bar_width - 20, 20, hp_bar_width, 20))
    pygame.draw.rect(surface, GREEN, (WIDTH - hp_bar_width - 20, 20, hp_bar_width * hp_ratio, 20))
    hp_text = font.render(f"HP: {player_hp}/{player_max_hp}", True, BLACK)
    surface.blit(hp_text, (WIDTH - hp_bar_width - 20, 50))

def draw_exp_bar(surface, player_exp, player_level):
    """繪製經驗條"""
    exp_bar_width = 200
    required_exp = 30 * (player_level ** 2)
    exp_ratio = player_exp / required_exp
    pygame.draw.rect(surface, BLACK, (20, 20, exp_bar_width, 10))
    pygame.draw.rect(surface, GREEN, (20, 20, exp_bar_width * exp_ratio, 10))

def draw_game_info(surface, player_level, current_wave, max_waves):
    """顯示遊戲基本資訊"""
    level_text = font.render(f"Level: {player_level}", True, BLACK)
    surface.blit(level_text, (20, 40))
    wave_text = font.render(f"Wave: {current_wave}/{max_waves}", True, BLACK)
    surface.blit(wave_text, (20, 100))

def draw_equipment_panel(surface, player_equipment, equipment_icons, equipment_descriptions):
    """繪製裝備欄"""
    panel_x = WIDTH - 300
    panel_y = 150
    panel_width = 280
    panel_height = 300
    pygame.draw.rect(surface, BLACK, (panel_x, panel_y, panel_width, panel_height), 2)
    for i, eq in enumerate(player_equipment):
        icon = equipment_icons.get(eq["name"], eq["name"])
        if eq["rare"]:
            icon += "★"
        txt_icon = equip_font.render(icon, True, BLACK)
        txt_desc = upgrade_font.render(equipment_descriptions.get(eq["name"], ""), True, BLACK)
        surface.blit(txt_icon, (panel_x + 10, panel_y + 10 + i * 50))
        surface.blit(txt_desc, (panel_x + 50, panel_y + 10 + i * 50))

def draw_pause_menu(screen):
    """繪製暫停選單"""
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))  # 半透明黑色背景
    screen.blit(overlay, (0, 0))

    font = pygame.font.Font(font_path, 50)  # 使用指定的中文字型
    options = ["繼續遊戲", "設定", "回到首頁"]
    option_y = HEIGHT // 2 - 50

    for option in options:
        text_surface = font.render(option, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(WIDTH // 2, option_y))
        screen.blit(text_surface, text_rect)
        option_y += 60

def draw_main_menu(screen):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((50, 50, 50, 255))
    title = upgrade_font.render("主選單", True, (255, 255, 255))
    overlay.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 100))
    option = upgrade_font.render("按 Enter 開始遊戲", True, (255, 255, 255))
    overlay.blit(option, (WIDTH // 2 - option.get_width() // 2, HEIGHT // 2))
    screen.blit(overlay, (0, 0))
    pygame.display.flip()




is_upgrading = False  # 是否進入升級狀態
upgrade_done = False  # 升級選項是否選擇完成

start_screen()

# ================= Main Game Loop =====================
running = True
while running:
    dt = clock.tick(60)
    # Use frame_surface for potential screen shake
    frame_surface = pygame.Surface((WIDTH, HEIGHT))
    frame_surface.fill(WHITE)
    current_time = pygame.time.get_ticks()
    update_floating_texts(dt)
    
    # Dynamic enemy spawn: if on-screen count below limit and remaining > 0, spawn new enemy
    while len(enemies) < max_enemies_on_screen and remaining_enemies_to_spawn > 0:
        enemies.append(spawn_enemy(current_wave))
        remaining_enemies_to_spawn -= 1

    # *** 插入炸彈更新和繪製代碼 ***
    for bomb in bombs:
        bomb.move()  # 更新炸彈位置
        if bomb.should_be_removed(): # 檢查炸彈是否需要被移除
          bombs.remove(bomb) # 從列表中移除炸彈
          continue # 繼續下一個炸彈的處理

        bomb.draw(frame_surface) # 在 frame_surface 上繪製炸彈

    # Energy Core effect: every 10 sec trigger electric shock (50 dmg within 150px)
    if any(e["name"] == "Energy Core" for e in player_equipment):
        if current_time - last_elec_time >= 10000:
            last_elec_time = current_time
            player_center = (player_x + player_size / 2, player_y + player_size / 2)
            for enemy in enemies:
                ex, ey = enemy.x, enemy.y
                enemy_center = (ex + enemy.size / 2, ey + enemy.size / 2)

                # 更新敵人的行為模式
                enemy.update_behavior(player_x, player_y, enemies)
                # 判斷是否觸發電擊
                if math.hypot(enemy_center[0] - player_center[0], enemy_center[1] - player_center[1]) < 150:
                    enemy.hp -= 50
                    add_floating_text("⚡ Electric Shock!", enemy_center, 1000)

    
    # ---------- Event Handling ----------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if game_state == "playing":
                    game_state = "paused"
                elif game_state == "paused":
                    game_state = "playing"

        # 如果處於暫停狀態，處理選單點擊
        elif game_state == "paused" and event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if HEIGHT // 2 - 50 <= mouse_y <= HEIGHT // 2 + 10:
                game_state = "playing"  # 點擊「繼續遊戲」
            elif HEIGHT // 2 + 10 <= mouse_y <= HEIGHT // 2 + 70:
                print("⚙️ [DEBUG] 設定功能尚未實作")  # 點擊「設定」
            elif HEIGHT // 2 + 70 <= mouse_y <= HEIGHT // 2 + 130:
                game_state = "menu"  # 點擊「回到首頁」

    # ---------- 主遊戲迴圈 ----------
    if game_state == "paused":
        draw_pause_menu(screen)  # 自定義的暫停選單函數
        pygame.display.flip()
        continue  # 暫停時不更新其他遊戲邏輯

    if game_state == "menu":
        draw_main_menu(screen)
        continue  # 當處於主選單狀態時，暫停其他遊戲邏輯




    # ---------- 使用 keyboard 函式庫 偵測空白鍵 ----------
    if keyboard.is_pressed("space"): #  <--- 使用 keyboard.is_pressed() 偵測空白鍵
        # Trigger sword attack if available
        if weapons["sword"] and not sword_swinging:
            sword_swinging = True
            sword_swing_start = current_time
            sword_hit_list = []
        # Trigger bullet attack if available
        if weapons["bullet"]:
            if current_time - last_bullet_time > bullet_cooldown:
                last_bullet_time = current_time
                muzzle_flash_time = current_time + muzzle_flash_duration
                player_center = (player_x+player_size/2, player_y+player_size/2)
                index, target_center = get_nearest_enemy(player_center)
                if target_center is not None:
                    dx = target_center[0]-player_center[0]
                    dy = target_center[1]-player_center[1]
                    primary_angle = math.atan2(dy, dx)
                else:
                    primary_angle = math.atan2(last_dir[1], last_dir[0]) 
                for i in range(bullet_count):
                    offset = random.uniform(-bullet_spread/2, bullet_spread/2)
                    angle = primary_angle + offset
                    direction = (math.cos(angle), math.sin(angle))
                    bullet = {"x": player_center[0], "y": player_center[1], "dir": direction}
                    bullets.append(bullet)
            
    
    # ---------- Player Movement & Direction ----------
    keys = pygame.key.get_pressed()
    dx = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
    dy = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
    if dx or dy:
        magnitude = math.hypot(dx, dy)
        last_dir = (dx/magnitude, dy/magnitude)
    if keys[pygame.K_LEFT]:
        player_x -= base_player_speed
    if keys[pygame.K_RIGHT]:
        player_x += base_player_speed
    if keys[pygame.K_UP]:
        player_y -= base_player_speed
    if keys[pygame.K_DOWN]:
        player_y += base_player_speed

    # *** 使用 pygame.key.get_pressed() 偵測空白鍵狀態 ***
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        # Trigger sword attack if available
        if weapons["sword"] and not sword_swinging:
            sword_swinging = True
            sword_swing_start = current_time
            sword_hit_list = []
        # Trigger bullet attack if available
        if weapons["bullet"]:
            if current_time - last_bullet_time > bullet_cooldown:
                last_bullet_time = current_time
                muzzle_flash_time = current_time + muzzle_flash_duration
                player_center = (player_x+player_size/2, player_y+player_size/2)
                index, target_center = get_nearest_enemy(player_center)
                if target_center is not None:
                    dx = target_center[0]-player_center[0]
                    dy = target_center[1]-player_center[1]
                    primary_angle = math.atan2(dy, dx)
                else:
                    primary_angle = math.atan2(last_dir[1], last_dir[0])
                for i in range(bullet_count):
                    offset = random.uniform(-bullet_spread/2, bullet_spread/2)
                    angle = primary_angle + offset
                    direction = (math.cos(angle), math.sin(angle))
                    bullet = {"x": player_center[0], "y": player_center[1], "dir": direction}
                    bullets.append(bullet)


    # Wind Boots: Increase speed by 15%
    if any(e["name"] == "Wind Boots" for e in player_equipment):
        player_speed = base_player_speed * 1.15
    else:
        player_speed = base_player_speed
    player_x = max(0, min(WIDTH - player_size, player_x))
    player_y = max(0, min(HEIGHT - player_size, player_y))
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    
    # ---------- Draw Player ----------
    pygame.draw.rect(frame_surface, BLUE, player_rect)
    
    # ---------- Draw Muzzle Flash ----------
    if current_time < muzzle_flash_time:
        flash_radius = 15
        pygame.draw.circle(frame_surface, ORANGE, (player_x+player_size//2, player_y+player_size//2), flash_radius)
    
    # ---------- Update & Draw Enemies ----------
    for enemy in enemies[:]:
        etype = enemy.etype
        if etype == "normal":
            base_speed_enemy = 2; size = enemy.size; color = RED; max_hp_val = 100
        elif etype == "elite":
            base_speed_enemy = 3; size = enemy.size; color = PURPLE; max_hp_val = 150
        elif etype == "boss":
            base_speed_enemy = 1; size = enemy.size*2; color = DARK_RED; max_hp_val = 500
        # Speed multiplier: increases with wave (multiplier = 1 + (current_wave-1)*0.1), except wave 1 fixed at 0.5
        if current_wave == 1:
            multiplier = 0.5
        else:
            multiplier = 1 + (current_wave - 1) * 0.1
        speed = base_speed_enemy * multiplier
        if player_x > enemy.x:
            enemy.x += speed
        elif player_x < enemy.x:
            enemy.x -= speed
        if player_y > enemy.y:
            enemy.y += speed
        elif player_y < enemy.y:
            enemy.y -= speed
        enemy_rect = pygame.Rect(enemy.x, enemy.y, size, size)
        pygame.draw.rect(frame_surface, color, enemy_rect)
        pygame.draw.rect(frame_surface, BLACK, (enemy.x, enemy.y-10, size, 5))
        hp_bar_width = size * (enemy.hp/max_hp_val)
        pygame.draw.rect(frame_surface, GREEN, (enemy.x, enemy.y-10, hp_bar_width, 5))
        # Collision with player
        if player_rect.colliderect(enemy_rect) and current_time - last_damage_time > player_damage_cooldown:
            blocked = False
            dodged = False
            if any(e["name"] == "Guardian Shield" for e in player_equipment):
                if random.random() < 0.5:
                    blocked = True
                    add_floating_text("🛡 Blocked!", (player_x, player_y-30))
            if any(e["name"] == "Wind Boots" for e in player_equipment):
                if random.random() < 0.1:
                    dodged = True
                    add_floating_text("MISS!", (player_x, player_y-30))
            if not dodged:
                if blocked:
                    player_hp -= 5
                else:
                    player_hp -= 10
            last_damage_time = current_time
        # Burning effect from Flame Sword
        if enemy.burn_time > 0:
            if current_time - enemy.last_burn_tick >= 1000:
                enemy.hp -= 5
                enemy.burn_time -= 1000
                enemy.last_burn_tick = current_time
                add_floating_text("🔥 Burning", (enemy.x, enemy.y-40), 800)
    
    # ---------- Sword Attack Mechanism (Melee) ----------
    if weapons["sword"] and sword_swinging:
        elapsed = current_time - sword_swing_start
        progress = min(1, elapsed / sword_duration)
        current_radius = progress * sword_range
        current_sector_angle = progress * sword_fan_angle
        player_center = (player_x+player_size/2, player_y+player_size/2)
        index, nearest_center = get_nearest_enemy(player_center)
        if nearest_center is not None:
            angle_center = math.atan2(nearest_center[1]-player_center[1],
                                      nearest_center[0]-player_center[0])
        else:
            angle_center = math.atan2(last_dir[1], last_dir[0])
        fan_points = [player_center]
        num_points = 20
        start_angle = angle_center - current_sector_angle/2
        for i in range(num_points+1):
            theta = start_angle + (current_sector_angle*i/num_points)
            x = player_center[0] + current_radius * math.cos(theta)
            y = player_center[1] + current_radius * math.sin(theta)
            fan_points.append((x, y))
        fan_color = (255, 0, 0, 200) if any(e["name"] == "Flame Sword" for e in player_equipment) else (255, 165, 0, 200)
        fan_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.polygon(fan_surface, fan_color, fan_points)
        frame_surface.blit(fan_surface, (0,0))
        for enemy in enemies[:]:
            if enemy in sword_hit_list:
                continue
            etype = enemy.etype
            size = enemy.size*2 if etype=="boss" else enemy.size
            enemy_center = (enemy.x+size/2, enemy.y+size/2)
            dx_e = enemy_center[0]-player_center[0]
            dy_e = enemy_center[1]-player_center[1]
            dist = math.hypot(dx_e, dy_e)
            if dist <= current_radius:
                enemy_angle = math.atan2(dy_e, dx_e)
                diff = abs((enemy_angle - angle_center + math.pi) % (2*math.pi) - math.pi)
                if diff <= current_sector_angle/2:
                    enemy.hp -= attack_damage
                    # Apply knockback: 20 pixels for normal/elite, 10 for boss.
                    knockback_force = 20 if enemy.etype != "boss" else 10
                    if dist > 0:
                        enemy.x += (dx_e/dist) * knockback_force
                        enemy.y += (dy_e/dist) * knockback_force
                    sword_hit_list.append(enemy)
                    if any(e["name"] == "Flame Sword" for e in player_equipment):
                        enemy.burn_time = 3000
                        enemy.last_burn_tick = current_time
                        add_floating_text("🔥 Burned", enemy_center, 1000)
                    if enemy.hp <= 0:
                        drop_equipment(enemy)
                        enemies.remove(enemy)
                        player_exp += 25
        if elapsed > sword_duration:
            sword_swinging = False
    
    # ---------- Bullet Attack Mechanism (Ranged) ----------
    if weapons["bullet"]:
        for bullet in bullets[:]:
            prev_pos = (bullet["x"], bullet["y"])
            bullet["x"] += bullet["dir"][0] * bullet_speed
            bullet["y"] += bullet["dir"][1] * bullet_speed
            pygame.draw.line(frame_surface, ORANGE, prev_pos, (bullet["x"], bullet["y"]), 2)
            pygame.draw.circle(frame_surface, ORANGE, (int(bullet["x"]), int(bullet["y"])), 5)
            if bullet["x"] < 0 or bullet["x"] > WIDTH or bullet["y"] < 0 or bullet["y"] > HEIGHT:
                bullets.remove(bullet)
                continue
            bullet_rect = pygame.Rect(bullet["x"]-5, bullet["y"]-5, 10, 10)
            for enemy in enemies[:]:
                etype = enemy.etype
                size = enemy.size*2 if etype=="boss" else enemy.size
                enemy_rect = pygame.Rect(enemy.x, enemy.y, size, size)
                if bullet_rect.colliderect(enemy_rect):
                    enemy.hp -= attack_damage
                    if any(e["name"] == "Explosive Shotgun" for e in player_equipment):
                        for other in enemies:
                            ox = other.x; oy = other.y
                            if math.hypot(ox - enemy.x, oy - enemy.y) < 50:
                                other.hp -= 5
                        add_floating_text("💥 Explosion!", (enemy.x, enemy.y), 800)
                        screen_shake_time = 300
                        screen_shake_intensity = 5
                    if enemy.hp <= 0:
                        drop_equipment(enemy)
                        enemies.remove(enemy)
                        player_exp += 25
                    if bullet in bullets:
                        bullets.remove(bullet)
                    break
    
    # ---------- Safety Check for Enemy Death ----------
    for enemy in enemies[:]:
        if enemy.hp <= 0:
            drop_equipment(enemy)
            enemies.remove(enemy)
            player_exp += 25
    
    # ---------- Draw Floating Texts ----------
    draw_floating_texts(frame_surface)
    
    # 呼叫 UI 繪製函數
    draw_hp_bar(frame_surface, player_hp, player_max_hp)
    draw_exp_bar(frame_surface, player_exp, player_level)
    draw_game_info(frame_surface, player_level, current_wave, max_waves)
    draw_equipment_panel(frame_surface, player_equipment, equipment_icons, equipment_descriptions)

    # Top-center: Remaining enemy count
    total_remaining = len(enemies) + remaining_enemies_to_spawn
    enemy_count_text = upgrade_font.render(f"Enemies Left: {total_remaining}", True, BLACK)
    frame_surface.blit(enemy_count_text, (WIDTH//2 - enemy_count_text.get_width()//2, 20))
    # Top-right: Equipment display
    equip_text = upgrade_font.render("Equipment:", True, BLACK)
    frame_surface.blit(equip_text, (WIDTH - 220, 80))
    for i, eq in enumerate(player_equipment):
        icon = equipment_icons.get(eq["name"], eq["name"])
        if eq["rare"]:
            icon += "★"
        txt = equip_font.render(icon, True, BLACK)
        frame_surface.blit(txt, (WIDTH - 220, 110 + i * 30))
    # Right-side: Equipment Info Panel
    panel_x = WIDTH - 300
    panel_y = 150
    panel_width = 280
    panel_height = 300
    pygame.draw.rect(frame_surface, BLACK, (panel_x, panel_y, panel_width, panel_height), 2)
    for i, eq in enumerate(player_equipment):
        icon = equipment_icons.get(eq["name"], eq["name"])
        if eq["rare"]:
            icon += "★"
        txt_icon = equip_font.render(icon, True, BLACK)
        txt_desc = upgrade_font.render(equipment_descriptions.get(eq["name"], ""), True, BLACK)
        frame_surface.blit(txt_icon, (panel_x + 10, panel_y + 10 + i * 50))
        frame_surface.blit(txt_desc, (panel_x + 50, panel_y + 10 + i * 50))
    
    # ---------- Screen Shake Effect ----------
    if screen_shake_time > 0:
        offset_x = random.randint(-int(screen_shake_intensity), int(screen_shake_intensity))
        offset_y = random.randint(-int(screen_shake_intensity), int(screen_shake_intensity))
        screen.blit(frame_surface, (offset_x, offset_y))
        screen_shake_time -= dt
    else:
        screen.blit(frame_surface, (0, 0))
    
    pygame.display.update()
    
    # ---------- Wave Check ----------
    if total_remaining == 0:
        current_wave += 1
        if current_wave > max_waves:
            win_surface = pygame.Surface((WIDTH, HEIGHT))
            win_surface.fill(WHITE)
            win_text = font.render("You cleared all waves!", True, GREEN)
            win_surface.blit(win_text, (WIDTH//2 - win_text.get_width()//2, HEIGHT//2 - win_text.get_height()//2))
            screen.blit(win_surface, (0, 0))
            pygame.display.update()
            pygame.time.delay(3000)
            running = False
        else:
            total_enemies_in_wave = 20
            remaining_enemies_to_spawn = total_enemies_in_wave
            enemies = []
    
    # ---------- Level Up Check ----------
    # Required EXP increases quadratically: required_exp = 30 * (player_level^2)
    # 在主遊戲循環內
    required_exp = 30 * (player_level ** 2)
    if player_exp >= required_exp:
        player_exp = 0
        is_upgrading = True
        upgrade_done = False

        # ----- 篩選可用的升級選項 -----
        available_upgrades = [ #  使用列表推導式，篩選出符合等級需求的升級選項
            option for option in upgrade_options_data if player_level >= option["level_required"]
        ]

        # ----- 限制升級選項數量 (例如最多顯示 3 個) -----
        import random #  如果使用 random.sample，需要 import random
        if len(available_upgrades) > 3:
            upgrade_choices = random.sample(available_upgrades, 3) #  從可用選項中隨機挑選 3 個
        else:
            upgrade_choices = available_upgrades #  如果可用選項少於 3 個，則全部顯示

        # 保留當前戰鬥畫面在 frame_surface 中（假設它已經包含所有戰鬥元素）
        while not upgrade_done:
            draw_upgrade_overlay(frame_surface, upgrade_choices, player_level) # 修改: 傳入 upgrade_choices 和 player_level

            # Pygame 事件迴圈，*只處理 QUIT 事件*
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                            pygame.quit(); sys.exit()

            # *** 使用 keyboard 函式庫 *直接偵測* 按鍵，並根據 upgrade_choices 判斷選項 ***
                for option in upgrade_choices: # 迴圈檢查每個升級選項
                    key = option["key_binding"] # 取得選項綁定的按鍵
                    if keyboard.is_pressed(key): # 偵測按鍵是否被按下
                        print(f"[DEBUG - 升級選單] 按下按鍵 {key}，選擇升級：{option['name']}") # 除錯訊息

                        # ----- 套用升級效果 -----
                        effect_code = option["effect"] # 取得升級效果程式碼字串
                        exec(effect_code) #  執行升級效果程式碼 (!!!  請務必仔細檢查 effect_code 的安全性 !!! )

                        upgrade_done = True # 完成升級選擇


        is_upgrading = False
        player_level += 1



    
    # ---------- Player Death Check ----------
    if player_hp <= 0:
        restart = end_screen()
        if restart:
            player_hp = player_max_hp = 100
            player_level = 1
            player_exp = 0
            current_wave = 1
            total_enemies_in_wave = 20
            remaining_enemies_to_spawn = total_enemies_in_wave
            enemies = []
            player_equipment = []
            weapons = {"sword": True, "bullet": False}
            sword_advanced = False
        else:
            pygame.quit(); sys.exit()


pygame.display.update()
pygame.quit()