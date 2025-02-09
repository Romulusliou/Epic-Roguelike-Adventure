import pygame
import random
import sys
import math

# ================= Initialization =====================
pygame.init()

# Set resolution to 1920x1080
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Epic Roguelike Adventure")

# Load fonts
try:
    font = pygame.font.Font("mingliu.ttc", 40)
except:
    font = pygame.font.SysFont("arial", 40)
try:
    equip_font = pygame.font.Font("seguiemj.ttf", 30)  # Font that supports emoji
except:
    print("Warning: Emoji font not found. Emoji may not display correctly.")
    equip_font = pygame.font.SysFont("arial", 30)
upgrade_font = pygame.font.SysFont("arial", 30)

# ================= Color Definitions ====================
WHITE    = (255, 255, 255)
RED      = (255, 0, 0)
GREEN    = (0, 255, 0)
BLUE     = (0, 0, 255)
BLACK    = (0, 0, 0)
ORANGE   = (255, 165, 0)
PURPLE   = (128, 0, 128)    # Elite enemy
DARK_RED = (139, 0, 0)      # Boss

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

# ================= Enemy Parameters =====================
total_enemies_in_wave = 20
remaining_enemies_to_spawn = total_enemies_in_wave
max_enemies_on_screen = 10
current_wave = 1
max_waves = 10
enemies = []  # 存放 Enemy 物件


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

# --- Bullet Parameters (Gun) ---
bullets = []  # Each bullet: {"x", "y", "dir": (dx,dy)}
bullet_cooldown = 300  # ms
last_bullet_time = 0
bullet_speed = 10
bullet_count = 3  # Number of bullets fired at once
bullet_spread = math.radians(30)  # Spread angle of 30°
last_dir = (0, -1)

class Enemy:
    def __init__(self, x, y, etype, wave):
        self.x = x
        self.y = y
        self.etype = etype
        self.set_attributes(etype, wave)
        self.burn_time = 0 
        self.last_burn_tick = 0

    def set_attributes(self, etype, wave):
        stats = {
            "normal": {"speed": 2, "size": 20, "color": RED, "max_hp": 100},
            "elite": {"speed": 3, "size": 20, "color": PURPLE, "max_hp": 150},
            "boss": {"speed": 1, "size": 40, "color": DARK_RED, "max_hp": 500}
        }[etype]
        self.speed = stats["speed"] * (0.5 if wave == 1 else 1 + (wave - 1) * 0.1)
        self.size = stats["size"]
        self.color = stats["color"]
        self.hp = self.max_hp = stats["max_hp"]

    def move_towards(self, target_x, target_y):
        if target_x > self.x:
            self.x += self.speed
        elif target_x < self.x:
            self.x -= self.speed
        if target_y > self.y:
            self.y += self.speed
        elif target_y < self.y:
            self.y -= self.speed

    def take_damage(self, amount):
        self.hp -= amount

    def apply_burn(self, current_time):
        if self.burn_time > 0 and current_time - self.last_burn_tick >= 1000:
            self.hp -= 5
            self.burn_time -= 1000
            self.last_burn_tick = current_time

    def draw(self, surface):
        rect = pygame.Rect(self.x, self.y, self.size, self.size)
        pygame.draw.rect(surface, self.color, rect)
        pygame.draw.rect(surface, BLACK, (self.x, self.y - 10, self.size, 5))
        hp_bar_width = self.size * (self.hp / self.max_hp) if self.max_hp else 0
        pygame.draw.rect(surface, GREEN, (self.x, self.y - 10, hp_bar_width, 5))
# === End Enemy Management Module ===

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
        title_text = font.render("Epic Roguelike Adventure", True, BLACK)
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
    # 選擇敵人類型，boss 波若尚未出現 boss，則設為 "boss"
        if current_wave == max_waves and not any(enemy.etype == "boss" for enemy in enemies):
            etype = "boss"
        else:
            etype = "elite" if random.random() < 0.3 else "normal"
    # 生成隨機位置（注意這裡的範圍可根據你的需求調整，或根據 enemy 的 size 來避免超出畫面）：
        x = random.randint(0, WIDTH - 100)
        y = random.randint(0, HEIGHT - 100)
        enemies.append(Enemy(x, y, etype, current_wave))
        remaining_enemies_to_spawn -= 1

    
    # Energy Core effect: every 10 sec trigger electric shock (50 dmg within 150px)
    if any(e["name"] == "Energy Core" for e in player_equipment):
        if current_time - last_elec_time >= 10000:
            last_elec_time = current_time
            player_center = (player_x+player_size/2, player_y+player_size/2)
            for enemy in enemies:
                ex, ey = enemy.x, enemy.y
                enemy_center = (ex+enemy.size/2, ey+enemy.size/2)
                if math.hypot(enemy_center[0]-player_center[0], enemy_center[1]-player_center[1]) < 150:
                    enemy.hp -= 50
                    add_floating_text("⚡ Electric Shock!", enemy_center, 1000)
    
    # ---------- Event Handling ----------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
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
    
    # ---------- Draw Player Interface ----------
    hp_bar_width = 200
    hp_ratio = player_hp / player_max_hp
    pygame.draw.rect(frame_surface, BLACK, (WIDTH - hp_bar_width - 20, 20, hp_bar_width, 20))
    pygame.draw.rect(frame_surface, GREEN, (WIDTH - hp_bar_width - 20, 20, hp_bar_width * hp_ratio, 20))
    hp_text = font.render(f"HP: {player_hp}/{player_max_hp}", True, BLACK)
    frame_surface.blit(hp_text, (WIDTH - hp_bar_width - 20, 50))
    
    exp_bar_width = 200
    # Use an increasing EXP curve: required_exp = 30 * (player_level ** 2)
    required_exp = 30 * (player_level ** 2)
    exp_ratio = player_exp / required_exp
    pygame.draw.rect(frame_surface, BLACK, (20, 20, exp_bar_width, 10))
    pygame.draw.rect(frame_surface, GREEN, (20, 20, exp_bar_width * exp_ratio, 10))
    
    level_text = font.render(f"Level: {player_level}", True, BLACK)
    frame_surface.blit(level_text, (20, 40))
    wave_text = font.render(f"Wave: {current_wave}/{max_waves}", True, BLACK)
    frame_surface.blit(wave_text, (20, 100))
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
    if player_exp >= required_exp:
        upgrade_done = False
        while not upgrade_done:
            upgrade_surface = pygame.Surface((WIDTH, HEIGHT))
            upgrade_surface.fill(WHITE)
            option1 = upgrade_font.render("1. Increase HP +20", True, BLACK)
            option2 = upgrade_font.render("2. Increase Attack +5", True, BLACK)
            if player_level >= 3:
                option3 = upgrade_font.render("3. Acquire Gun", True, BLACK)
            else:
                option3 = upgrade_font.render("3. (Locked)", True, BLACK)
            prompt = upgrade_font.render("Choose upgrade (Press 1, 2, or 3)", True, BLACK)
            upgrade_surface.blit(option1, (100, 150))
            upgrade_surface.blit(option2, (100, 210))
            upgrade_surface.blit(option3, (100, 270))
            upgrade_surface.blit(prompt, (100, 330))
            screen.blit(upgrade_surface, (0, 0))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        player_max_hp += 20
                        player_hp = player_max_hp
                        upgrade_done = True
                    elif event.key == pygame.K_2:
                        attack_damage += 5
                        upgrade_done = True
                    elif event.key == pygame.K_3 and player_level >= 3:
                        weapons["bullet"] = True
                        upgrade_done = True
        player_level += 1
        player_exp = 0
    
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
        else:
            pygame.quit(); sys.exit()

pygame.display.update()
pygame.quit()
