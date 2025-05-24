import pygame
import sys
import random
import math
import os 
import keyboard 
import time

# --- Module-level placeholders for settings (to be updated by run_game) ---
module_screen = None
module_WIDTH, module_HEIGHT = 0, 0
module_fonts = {} 
module_COLOR_DICT = {} 
module_BLACK = (0,0,0)
module_WHITE = (255,255,255)
module_GREEN = (0,255,0)
module_RED = (255,0,0)
module_ORANGE = (255,165,0)
module_BLUE = (0,0,255)
module_CYAN = (0,255,255)
module_PINK = (255,192,203)
module_DARK_RED = (139,0,0)
module_PURPLE = (128,0,128)

# --- Module-level Game Data ---
UPGRADE_OPTIONS_DATA = [ 
    {"type": "stat", "subtype": "hp", "name": "強化生命值", "description": "永久增加 20 點生命值上限，提升生存能力。", "effect": "player_max_hp += 20", "level_required": 1, "display_color": "GREEN", "key_binding": "1"},
    {"type": "stat", "subtype": "attack", "name": "強化攻擊力", "description": "永久增加 5 點基礎攻擊力，提升傷害輸出。", "effect": "attack_damage += 5", "level_required": 1, "display_color": "ORANGE", "key_binding": "2"},
    {"type": "stat", "subtype": "speed", "name": "強化移動速度", "description": "永久提升 10% 移動速度，更加靈活。", "effect": "base_player_speed *= 1.1", "level_required": 2, "display_color": "YELLOW", "key_binding": "3"},
    {"type": "stat", "subtype": "hp_regen", "name": "強化生命回復", "description": "永久提升 1 點/秒 生命回復速度，增強續戰力。", "effect": "player_hp_regen += 1", "level_required": 3, "display_color": "CYAN", "key_binding": "4"},
    {"type": "stat", "subtype": "crit_rate", "name": "強化暴擊率", "description": "永久提升 5% 暴擊率，造成更高爆發傷害。", "effect": "player_crit_rate += 0.05", "level_required": 4, "display_color": "RED", "key_binding": "5"},
    {"type": "stat", "subtype": "dodge_rate", "name": "強化閃避率", "description": "永久提升 2% 閃避率，更不容易受到傷害。", "effect": "player_dodge_rate += 0.02", "level_required": 5, "display_color": "PINK", "key_binding": "6"},
    {"type": "bullet", "subtype": "gun", "name": "解鎖基礎槍", "description": "獲得基礎槍，遠程攻擊能力UP！", "effect": "weapons['bullet'] = True", "level_required": 1, "display_color": "BLUE", "key_binding": "7"},
]

EQUIPMENT_ICONS = {
    "Flame Sword": "🔥", "Explosive Shotgun": "💥", "Guardian Shield": "🛡",
    "Wind Boots": "🌪", "Energy Core": "⚡"
}
EQUIPMENT_DESCRIPTIONS = {
    "Flame Sword": "Sword attacks inflict burning (3s, 5 dmg/sec).",
    "Explosive Shotgun": "Bullets cause explosions with splash damage.",
    "Guardian Shield": "50% chance to block damage (half damage).",
    "Wind Boots": "Increase speed by 15% and 10% chance to dodge attacks.",
    "Energy Core": "Triggers electric shock every 10s (50 dmg) to nearby enemies."
}

ENEMY_STATS_DATA = { 
    "normal": {"speed": 2, "size": 20, "color_name": "RED", "max_hp": 100},
    "elite": {"speed": 3, "size": 20, "color_name": "PURPLE", "max_hp": 150},
    "swift": {"speed": 4, "size": 18, "color_tuple": (0, 200, 200), "max_hp": 80},
    "tank": {"speed": 1, "size": 30, "color_tuple": (100, 100, 100), "max_hp": 200},
    "healer": {"speed": 2, "size": 22, "color_name": "CYAN", "max_hp": 120},
    "bomber": {"speed": 2, "size": 24, "color_name": "ORANGE", "max_hp": 100},
    "summoner": {"speed": 1.5, "size": 26, "color_name": "PINK", "max_hp": 130}, 
    "boss": {"speed": 1, "size": 40, "color_name": "DARK_RED", "max_hp": 500}
}

WAVE_ENEMY_TYPES_DATA = {
    1: ["normal"], 3: ["normal", "elite", "swift"], 5: ["normal", "elite", "swift", "tank"],
    7: ["normal", "elite", "swift", "tank", "healer"],
    9: ["normal", "elite", "swift", "tank", "healer", "bomber", "summoner"]
}
MAX_WAVES_CONFIG = 10 
_current_wave_module_level = 0 # Used by Enemy.summon_enemy

# --- Classes ---
class Bomb: # Depends on module_COLOR_DICT (set in run_game)
    def __init__(self, x, y, target_x, target_y, enemies_list_ref): 
        self.x, self.y = x, y
        self.target_x, self.target_y = target_x, target_y
        self.speed = 5  
        self.exploded = False
        self.explosion_radius, self.damage = 50, 50
        self.enemies_list_ref = enemies_list_ref

    def move(self):
        if not self.exploded:
            dx, dy = self.target_x - self.x, self.target_y - self.y
            dist = math.hypot(dx, dy)
            if dist > 0: self.x += (dx/dist)*self.speed; self.y += (dy/dist)*self.speed
            if dist < 5: self.explode()

    def explode(self):
        self.exploded = True
        for enemy_obj in self.enemies_list_ref:  
            if math.hypot(enemy_obj.x-self.x, enemy_obj.y-self.y) < self.explosion_radius: enemy_obj.hp -= self.damage

    def draw(self, surface):
        color_tuple = module_COLOR_DICT.get("YELLOW",(255,255,0)) if self.exploded else module_COLOR_DICT.get("RED",(255,0,0))
        if self.exploded: pygame.draw.circle(surface, color_tuple, (int(self.x), int(self.y)), self.explosion_radius, 2)
        else: pygame.draw.circle(surface, color_tuple, (int(self.x), int(self.y)), 5)

    def should_be_removed(self): return self.exploded

class Enemy: # Depends on module_COLOR_DICT, _current_wave_module_level, module_RED
    def __init__(self, x, y, etype, wave, bombs_list_ref, enemies_list_ref_main, current_wave_for_enemy):
        self.x, self.y, self.etype, self.wave = x, y, etype, wave
        self.bombs_list_ref = bombs_list_ref 
        self.enemies_list_ref_main = enemies_list_ref_main
        self.current_wave_for_enemy_logic = current_wave_for_enemy 
        self.set_attributes()
        self.burn_time, self.last_burn_tick = 0,0
        self.attack_cooldown, self.summon_cooldown, self.shield = 0,0,0
        self.direction = random.choice([-1,1])

    def set_attributes(self): 
        stats = ENEMY_STATS_DATA[self.etype]
        self.speed_multiplier = (0.5 if self.wave == 1 else 1 + (self.wave - 1) * 0.1)
        self.base_speed = stats["speed"]
        self.speed = self.base_speed * self.speed_multiplier
        self.size = stats["size"]
        self.color = stats.get("color_tuple") or module_COLOR_DICT.get(stats.get("color_name"), module_RED)
        self.hp = self.max_hp = stats["max_hp"]

    def move_towards(self, target_x, target_y):
        if target_x > self.x: self.x += self.speed
        elif target_x < self.x: self.x -= self.speed
        if target_y > self.y: self.y += self.speed
        elif target_y < self.y: self.y -= self.speed
    
    def update_behavior(self, target_x, target_y): 
        global _current_wave_module_level 
        self.move_towards(target_x, target_y) 
        current_stats = ENEMY_STATS_DATA[self.etype] 
        current_base_speed_calculated = current_stats["speed"] * self.speed_multiplier

        if self.etype == "elite":
            if self.attack_cooldown <= 0: self.speed = current_base_speed_calculated * 2; self.attack_cooldown = 60 
            if self.attack_cooldown > 0: self.attack_cooldown -=1 
            if self.speed > current_base_speed_calculated and self.attack_cooldown <=0 : self.speed = current_base_speed_calculated
        elif self.etype == "swift":
            self.x += self.direction * self.speed 
            if random.random() < 0.02: self.direction *= -1
            if self.attack_cooldown <= 0 and self.is_near(target_x, target_y, 50): self.speed = current_base_speed_calculated * 3; self.attack_cooldown = 80
            if self.attack_cooldown > 0 : self.attack_cooldown -=1 
            if self.speed > current_base_speed_calculated and self.attack_cooldown <=0 : self.speed = current_base_speed_calculated
        elif self.etype == "tank":
            if pygame.time.get_ticks() % 5000 < 100: self.shield = 1 
        elif self.etype == "healer":
            self.x += random.uniform(-1,1)*self.speed; self.y += random.uniform(-1,1)*self.speed
            self.heal_allies()
        elif self.etype == "bomber":
            if self.attack_cooldown <= 0: self.throw_bomb(target_x, target_y); self.attack_cooldown = 120
            else: self.attack_cooldown -= 1
        elif self.etype == "summoner":
            if self.summon_cooldown <= 0: self.summon_enemy(); self.summon_cooldown = 200
            else: self.summon_cooldown -=1
            if self.hp < self.max_hp*0.5: self.x += (self.x-target_x)*0.1 
        elif self.etype == "boss":
            if random.random()<0.01: self.throw_bomb(target_x,target_y)
            if random.random()<0.005: self.summon_enemy()
            if random.random()<0.002: self.speed = current_base_speed_calculated*2; self.attack_cooldown=60
            if self.attack_cooldown > 0 : self.attack_cooldown -=1 ;
            if self.speed > current_base_speed_calculated and self.attack_cooldown <=0 : self.speed = current_base_speed_calculated

    def apply_burn(self, current_time_ms):
        if self.burn_time > 0 and current_time_ms - self.last_burn_tick >= 1000:
            self.hp -= 5; self.burn_time -= 1000; self.last_burn_tick = current_time_ms

    def draw(self, surface):
        rect = pygame.Rect(self.x, self.y, self.size, self.size)
        pygame.draw.rect(surface, self.color, rect)
        pygame.draw.rect(surface, module_BLACK,(self.x,self.y-10,self.size,5))
        hp_w = self.size*(self.hp/self.max_hp) if self.max_hp>0 else 0
        pygame.draw.rect(surface,module_GREEN,(self.x,self.y-10,hp_w,5))

    def is_near(self, tx, ty, r): return math.hypot(self.x-tx,self.y-ty)<r
    def throw_bomb(self,tx,ty): self.bombs_list_ref.append(Bomb(self.x,self.y,tx,ty,self.enemies_list_ref_main)) 
    def summon_enemy(self): self.enemies_list_ref_main.append(Enemy(self.x+random.randint(-30,30),self.y+random.randint(-30,30),"normal",_current_wave_module_level, self.bombs_list_ref,self.enemies_list_ref_main, _current_wave_module_level))
    def heal_allies(self): 
        for e in self.enemies_list_ref_main: 
            if e!=self and self.is_near(e.x,e.y,100):e.hp=min(e.max_hp,e.hp+10)

# --- Helper Functions ---
def add_floating_text_local(floating_texts_list, text, pos, duration=1000): 
    if module_fonts.get('upgrade') and module_BLACK is not None:
        floating_texts_list.append({"text_surface": module_fonts['upgrade'].render(text, True, module_BLACK), "pos": pos, "timer": duration})

def update_floating_texts_local(dt, floating_texts_list): 
    for obj in floating_texts_list[:]:
        obj["timer"] -= dt
        if obj["timer"] <= 0: floating_texts_list.remove(obj)

def draw_floating_texts_local(surface, floating_texts_list): 
    for obj in floating_texts_list: surface.blit(obj["text_surface"], obj["pos"])

def get_nearest_enemy_local(player_center, current_enemies_list):
    idx, center, min_d = None, None, float('inf')
    for i, enemy_obj in enumerate(current_enemies_list):
        enemy_c = (enemy_obj.x + enemy_obj.size/2, enemy_obj.y + enemy_obj.size/2)
        dist = math.hypot(player_center[0] - enemy_c[0], player_center[1] - enemy_c[1])
        if dist < min_d: min_d, idx, center = dist, i, enemy_c
    return idx, center

def start_screen_local(game_clock_ref): 
    wait = True; clock_local = game_clock_ref 
    while wait:
        for event_s in pygame.event.get():
            if event_s.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event_s.type == pygame.KEYDOWN and event_s.key == pygame.K_RETURN: wait = False
        
        fr = pygame.Surface((module_WIDTH,module_HEIGHT));fr.fill(module_WHITE)
        t_txt=module_fonts['main'].render("穿越成為成最強冒險家",True,module_BLACK)
        p_txt=module_fonts['main'].render("Press ENTER to Start",True,module_BLACK)
        fr.blit(t_txt,(module_WIDTH//2-t_txt.get_width()//2,module_HEIGHT//2-t_txt.get_height()-20))
        fr.blit(p_txt,(module_WIDTH//2-p_txt.get_width()//2,module_HEIGHT//2+20))
        module_screen.blit(fr,(0,0));pygame.display.update(); clock_local.tick(15) 

def end_screen_local(game_clock_ref):
    wait=True; clock_local = game_clock_ref
    while wait:
        for event_e in pygame.event.get():
            if event_e.type==pygame.QUIT:pygame.quit();sys.exit()
            if event_e.type==pygame.KEYDOWN:
                if event_e.key==pygame.K_r:return True
                elif event_e.key==pygame.K_q:return False
        
        fr=pygame.Surface((module_WIDTH,module_HEIGHT));fr.fill(module_WHITE)
        p_txt=module_fonts['main'].render("Game Over",True,module_RED)
        o_txt=module_fonts['upgrade'].render("Press R to Restart or Q to Quit",True,module_BLACK)
        fr.blit(p_txt,(module_WIDTH//2-p_txt.get_width()//2,module_HEIGHT//2-p_txt.get_height()))
        fr.blit(o_txt,(module_WIDTH//2-o_txt.get_width()//2,module_HEIGHT//2+20))
        module_screen.blit(fr,(0,0));pygame.display.update(); clock_local.tick(15)

def draw_hp_bar_local(surface, hp, max_hp):
    bar_w=200;ratio=hp/max_hp if max_hp>0 else 0
    pygame.draw.rect(surface,module_BLACK,(module_WIDTH-bar_w-20,20,bar_w,20))
    pygame.draw.rect(surface,module_GREEN,(module_WIDTH-bar_w-20,20,bar_w*ratio,20))
    hp_s=module_fonts['main'].render(f"HP: {int(hp)}/{int(max_hp)}",True,module_BLACK)
    surface.blit(hp_s,(module_WIDTH-bar_w-20,50))

def draw_exp_bar_local(surface, exp, lvl):
    bar_w=200;req_exp=30*(lvl**2)if lvl>0 else 30;ratio=exp/req_exp if req_exp>0 else 0
    pygame.draw.rect(surface,module_BLACK,(20,20,bar_w,10))
    pygame.draw.rect(surface,module_GREEN,(20,20,bar_w*ratio,10))

def draw_game_info_local(surface, lvl, cr_wave, max_w):
    lvl_s=module_fonts['main'].render(f"Level: {lvl}",True,module_BLACK);surface.blit(lvl_s,(20,40))
    wave_s=module_fonts['main'].render(f"Wave: {cr_wave}/{max_w}",True,module_BLACK);surface.blit(wave_s,(20,100))

def draw_equipment_panel_local(surface, p_eq_list):
    px,py,pw,ph=module_WIDTH-300,150,280,300
    pygame.draw.rect(surface,module_BLACK,(px,py,pw,ph),2)
    for i,eq_item in enumerate(p_eq_list):
        icon=EQUIPMENT_ICONS.get(eq_item["name"],eq_item["name"])+("★"if eq_item["rare"]else"")
        icon_s=module_fonts['equip'].render(icon,True,module_BLACK)
        desc_s=module_fonts['upgrade_small'].render(EQUIPMENT_DESCRIPTIONS.get(eq_item["name"],""),True,module_BLACK)
        surface.blit(icon_s,(px+10,py+10+i*50));surface.blit(desc_s,(px+50,py+10+i*50))

def draw_pause_menu_local(current_screen_surf):
    ov=pygame.Surface((module_WIDTH,module_HEIGHT),pygame.SRCALPHA);ov.fill((0,0,0,180));current_screen_surf.blit(ov,(0,0))
    m_font=module_fonts['main'] 
    opts=["繼續遊戲","設定","回到首頁"];opt_y=module_HEIGHT//2-50
    for i,opt_txt in enumerate(opts):
        txt_s=m_font.render(opt_txt,True,module_WHITE);txt_r=txt_s.get_rect(center=(module_WIDTH//2,opt_y+i*60))
        current_screen_surf.blit(txt_s,txt_r)

def draw_main_menu_local(current_screen_surf):
    ov=pygame.Surface((module_WIDTH,module_HEIGHT));ov.fill(module_COLOR_DICT.get("GRAY_DARK",(50,50,50)))
    tit_s=module_fonts['upgrade'].render("主選單",True,module_WHITE)
    ov.blit(tit_s,(module_WIDTH//2-tit_s.get_width()//2,module_HEIGHT//2-100))
    opt_s=module_fonts['upgrade'].render("按 Enter 開始遊戲",True,module_WHITE)
    ov.blit(opt_s,(module_WIDTH//2-opt_s.get_width()//2,module_HEIGHT//2));current_screen_surf.blit(ov,(0,0))

def draw_upgrade_overlay_local(base_surf, opts_list, p_lvl):
    overlay_f=pygame.Surface((module_WIDTH,module_HEIGHT),pygame.SRCALPHA);overlay_f.fill((0,0,0,120));base_surf.blit(overlay_f,(0,0))
    box_w,box_h,space=300,200,50;total_w=len(opts_list)*box_w+(len(opts_list)-1)*space
    sx=(module_WIDTH-total_w)//2;sy=(module_HEIGHT-box_h)//2
    for i,opt in enumerate(opts_list):
        rect_x=sx+i*(box_w+space);opt_r=pygame.Rect(rect_x,sy,box_w,box_h)
        pygame.draw.rect(base_surf,module_BLACK,opt_r,2)
        color_n=opt.get("display_color","GREEN");rgb_c=module_COLOR_DICT.get(color_n,module_GREEN)
        pygame.draw.rect(base_surf,rgb_c,(opt_r.x+20,opt_r.y+20,box_w-40,box_h-80))
        nm_s=module_fonts['upgrade'].render(opt["name"],True,module_BLACK);base_surf.blit(nm_s,(opt_r.x+20,opt_r.y+box_h-100))
        desc_s=module_fonts['upgrade_small'].render(opt["description"],True,module_BLACK);base_surf.blit(desc_s,(opt_r.x+20,opt_r.y+box_h-60))
        key_s=module_fonts['upgrade'].render(f"Press {opt['key_binding']}",True,module_BLACK);base_surf.blit(key_s,(opt_r.x+20,opt_r.y+box_h-30))
    pr_s=module_fonts['upgrade'].render("Choose upgrade",True,module_BLACK);base_surf.blit(pr_s,(module_WIDTH//2-pr_s.get_width()//2,sy+box_h+20))

def spawn_enemy_local(wave, bombs_list_ref, enemies_list_ref): 
    global _current_wave_module_level 
    types = WAVE_ENEMY_TYPES_DATA.get(wave)
    if types is None:
        keys = sorted(WAVE_ENEMY_TYPES_DATA.keys())
        for k in reversed(keys):
            if wave >= k: types = WAVE_ENEMY_TYPES_DATA[k]; break
    etype = random.choice(types if types else ["normal"])
    if wave == MAX_WAVES_CONFIG and not any(e.etype == "boss" for e in enemies_list_ref): etype = "boss"
    x = random.randint(0, module_WIDTH - 100); y = random.randint(0, module_HEIGHT - 100)
    return Enemy(x,y,etype,wave,bombs_list_ref,enemies_list_ref, _current_wave_module_level)

def drop_equipment_local(enemy_obj, p_equipment_list): 
    def add_eq(name, is_rare):
        if not any(eq["name"]==name for eq in p_equipment_list): p_equipment_list.append({"name":name,"rare":is_rare})
    if enemy_obj.etype in ["normal","elite"] and random.random()<0.1: add_eq(random.choice(list(EQUIPMENT_ICONS.keys())),False)
    elif enemy_obj.etype=="boss" and random.random()<0.5: add_eq(random.choice(list(EQUIPMENT_ICONS.keys())),True)

# --- Main Game Function ---
def run_game(settings, game_clock_ref): 
    global _current_wave_module_level, module_screen, module_WIDTH, module_HEIGHT, module_fonts, module_COLOR_DICT, module_BLACK, module_WHITE, module_GREEN, module_RED, module_ORANGE, module_BLUE, module_CYAN, module_PINK, module_DARK_RED, module_PURPLE

    module_screen = settings['screen']; module_WIDTH = settings['WIDTH']; module_HEIGHT = settings['HEIGHT']
    module_fonts = settings['fonts']; module_COLOR_DICT = settings['colors'] 
    module_BLACK=module_COLOR_DICT.get("BLACK",(0,0,0));module_WHITE=module_COLOR_DICT.get("WHITE",(255,255,255));module_GREEN=module_COLOR_DICT.get("GREEN",(0,255,0));module_RED=module_COLOR_DICT.get("RED",(255,0,0));module_ORANGE=module_COLOR_DICT.get("ORANGE",(255,165,0));module_BLUE=module_COLOR_DICT.get("BLUE",(0,0,255));module_CYAN=module_COLOR_DICT.get("CYAN",(0,255,255));module_PINK=module_COLOR_DICT.get("PINK",(255,192,203));module_DARK_RED=module_COLOR_DICT.get("DARK_RED",(139,0,0));module_PURPLE=module_COLOR_DICT.get("PURPLE",(128,0,128))

    game_st="menu";px,py=module_WIDTH//2,module_HEIGHT//2;base_spd=5.0;p_size=40;php,pm_hp=100,100;p_lvl,p_exp=1,0
    php_regen,pc_rate,pd_rate=0.0,0.0,0.0;p_rect=pygame.Rect(px,py,p_size,p_size)
    
    enemies_l_ingame,bombs_l_ingame,p_eq_ingame,bullets_l_ingame = [],[],[],[]
    floating_texts_l_ingame = [] 
    
    rem_en_spawn=0;max_en_screen=10;_current_wave_module_level=0
    wpns,atk_dmg={"sword":True,"bullet":False},25
    swd_swing,swd_start_t,swd_hit=False,0,[]
    last_b_time,bullet_cooldown_val,b_spd_cfg,b_count_cfg,b_spread_cfg=0,300,10.0,3,math.radians(30.0) 
    p_last_dir=(0.0,-1.0)
    mflash_end_t,mflash_dur=0,100;sshake_end_t,sshake_int=0,0 
    last_p_dmg_t,last_ec_t=0,0;is_upg,upg_done=False,False
    player_damage_cooldown = 500 
    bullet_cooldown = 300 

    def reset_state_local_ingame(): 
        nonlocal px,py,php,pm_hp,p_lvl,p_exp,base_spd,php_regen,pc_rate,pd_rate,enemies_l_ingame,bombs_l_ingame,rem_en_spawn,atk_dmg,p_eq_ingame,wpns,swd_swing,p_last_dir,game_st,is_upg,upg_done,last_p_dmg_t,last_ec_t, bullets_l_ingame, floating_texts_l_ingame
        global _current_wave_module_level
        px,py=module_WIDTH//2,module_HEIGHT//2;php,pm_hp=100,100;p_lvl,p_exp=1,0;base_spd=5.0;php_regen,pc_rate,pd_rate=0.0,0.0,0.0;atk_dmg=25
        enemies_l_ingame,bombs_l_ingame,bullets_l_ingame,floating_texts_l_ingame=[],[];_current_wave_module_level=0;p_eq_ingame=[]
        wpns={"sword":True,"bullet":False};swd_swing,p_last_dir=False,(0.0,-1.0);is_upg,upg_done=False,False;last_p_dmg_t,last_ec_t=0,0

    def next_wave_local_ingame(): 
        nonlocal rem_en_spawn,enemies_l_ingame
        global _current_wave_module_level
        _current_wave_module_level+=1;rem_en_spawn=15+(_current_wave_module_level*5);enemies_l_ingame=[]
        print(f"Wave {_current_wave_module_level} - Spawning {rem_en_spawn} enemies.")

    if game_st=="menu":start_screen_local(game_clock_ref)
    
    running=True
    while running:
        dt=game_clock_ref.tick(60);now=pygame.time.get_ticks();frame=pygame.Surface((module_WIDTH,module_HEIGHT));frame.fill(module_WHITE)
        update_floating_texts_local(dt, floating_texts_l_ingame)
        
        for evt in pygame.event.get():
            if evt.type==pygame.QUIT:running=False
            elif evt.type==pygame.KEYDOWN:
                if evt.key==pygame.K_ESCAPE:
                    if game_st=="playing":game_st="paused"
                    elif game_st=="paused":game_st="playing"
            if game_st=="paused" and evt.type==pygame.MOUSEBUTTONDOWN:
                mx,my=pygame.mouse.get_pos()
                if(module_WIDTH//2-100<=mx<=module_WIDTH//2+100):
                    if(module_HEIGHT//2-50<=my<=module_HEIGHT//2-10):game_st="playing" 
                    elif(module_HEIGHT//2+10<=my<=module_HEIGHT//2+50):print("Settings clicked - placeholder")
                    elif(module_HEIGHT//2+70<=my<=module_HEIGHT//2+110):reset_state_local_ingame();game_st="menu";start_screen_local(game_clock_ref)
        
        if game_st=="menu":
            draw_main_menu_local(module_screen)
            if pygame.key.get_pressed()[pygame.K_RETURN]:reset_state_local_ingame();next_wave_local_ingame();game_st="playing"
            pygame.display.flip();continue
        if game_st=="paused":draw_pause_menu_local(module_screen);pygame.display.flip();continue

        if rem_en_spawn>0 and len(enemies_l_ingame)<max_en_screen:
            enemies_l_ingame.append(spawn_enemy_local(_current_wave_module_level,bombs_l_ingame,enemies_l_ingame))
            rem_en_spawn-=1
        for b_obj in bombs_l_ingame[:]: b_obj.move(); 
            if b_obj.should_be_removed():bombs_l_ingame.remove(b_obj)
            else:b_obj.draw(frame)
        if any(eq["name"]=="Energy Core" for eq in p_eq_ingame)and now-last_ec_t>=10000:
            last_ec_t=now;p_c=(px+p_size/2,py+p_size/2)
            for en in enemies_l_ingame:ec=(en.x+en.size/2,en.y+en.size/2);
                if math.hypot(ec[0]-p_c[0],ec[1]-p_c[1])<150:en.hp-=50;add_floating_text_local(floating_texts_l_ingame,"⚡ Shock!",ec)
        if keyboard.is_pressed("space"):
            if wpns["sword"]and not swd_swing:swd_swing=True;swd_start_t=now;swd_hit=[]
            if wpns["bullet"]and(now-last_b_time>bullet_cooldown_val):
                last_b_time=now;mflash_end_t=now+mflash_dur;p_c=(px+p_size/2,py+p_size/2)
                _,tc=get_nearest_enemy_local(p_c,enemies_l_ingame);aim_a=math.atan2(p_last_dir[1],p_last_dir[0])
                if tc:aim_a=math.atan2(tc[1]-p_c[1],tc[0]-p_c[0])
                for _ in range(b_count_cfg):bullets_l_ingame.append({"x":p_c[0],"y":p_c[1],"dir":(math.cos(aim_a+random.uniform(-b_spread_cfg/2,b_spread_cfg/2)),math.sin(aim_a+random.uniform(-b_spread_cfg/2,b_spread_cfg/2)))})
        kmv=pygame.key.get_pressed();dxm,dym=0.0,0.0
        if kmv[pygame.K_LEFT]:dxm-=1.0;
        if kmv[pygame.K_RIGHT]:dxm+=1.0
        if kmv[pygame.K_UP]:dym-=1.0;
        if kmv[pygame.K_DOWN]:dym+=1.0
        eff_spd=base_spd*(1.15 if any(e["name"]=="Wind Boots" for e in p_eq_ingame)else 1.0)
        if dxm!=0.0 or dym!=0.0:m=math.hypot(dxm,dym);p_last_dir=(dxm/m,dym/m);px+=p_last_dir[0]*eff_spd;py+=p_last_dir[1]*eff_spd
        px=max(0,min(module_WIDTH-p_size,px));py=max(0,min(module_HEIGHT-p_size,py));p_rect.topleft=(px,py)
        pygame.draw.rect(frame,module_BLUE,p_rect)
        if now<mflash_end_t:pygame.draw.circle(frame,module_ORANGE,p_rect.center,15)
        for en in enemies_l_ingame[:]:
            en.update_behavior(px,py);en.draw(frame)
            if p_rect.colliderect(pygame.Rect(en.x,en.y,en.size,en.size))and now-last_p_dmg_t>player_damage_cooldown:
                blk,ddg=False,False
                if any(e["name"]=="Guardian Shield" for e in p_eq_ingame)and random.random()<0.5:blk=True;add_floating_text_local(floating_texts_l_ingame,"🛡 Blocked!",p_rect.topleft)
                if random.random()<(pd_rate+(0.1 if any(e["name"]=="Wind Boots" for e in p_eq_ingame)else 0)):ddg=True;add_floating_text_local(floating_texts_l_ingame,"MISS!",p_rect.topleft)
                if not ddg:php-=(5 if blk else 10)
                last_p_dmg_t=now
            en.apply_burn(now)
            if en.hp<=0:drop_equipment_local(en,p_eq_ingame);enemies_l_ingame.remove(en);p_exp+=25
        if swd_swing:
            el_sw=now-swd_start_t;prog=min(1.0,el_sw/sword_duration);p_c=p_rect.center
            c_r=prog*sword_range;c_a=prog*sword_fan_angle;aim_a=math.atan2(p_last_dir[1],p_last_dir[0])
            _,near_c=get_nearest_enemy_local(p_c,enemies_l_ingame);
            if near_c:aim_a=math.atan2(near_c[1]-p_c[1],near_c[0]-p_c[0])
            arc_s=aim_a-c_a/2;arc_ps=[p_c]+[(p_c[0]+c_r*math.cos(arc_s+c_a*i/20),p_c[1]+c_r*math.sin(arc_s+c_a*i/20))for i in range(21)]
            s_cn="RED_TRANSPARENT" if any(e["name"]=="Flame Sword" for e in p_eq_ingame) else "ORANGE_TRANSPARENT"
            s_c=module_colors_dict.get(s_cn,(255,165,0,100));
            if len(arc_ps)>2:pygame.draw.polygon(frame,s_c,arc_ps)
            for eo in enemies_l_ingame[:]:
                if eo in swd_hit:continue
                e_c=(eo.x+eo.size/2,eo.y+eo.size/2);d=math.hypot(e_c[0]-p_c[0],e_c[1]-p_c[1])
                if d<=c_r:
                    angle_e=math.atan2(e_c[1]-p_c[1],e_c[0]-p_c[0]);angle_d=(angle_e-aim_a+math.pi)%(2*math.pi)-math.pi
                    if abs(angle_d)<=c_a/2:
                        eo.hp-=atk_dmg;swd_hit.append(eo)
                        if any(e["name"]=="Flame Sword" for e in p_eq_ingame):eo.burn_time=3000;eo.last_burn_tick=now;add_floating_text_local(floating_texts_l_ingame,"🔥 Burned",e_c)
                        if eo.hp<=0:drop_equipment_local(eo,p_eq_ingame);enemies_l_ingame.remove(eo);p_exp+=25
            if el_sw>sword_duration:swd_swing=False
        for bllt in bullets_l_ingame[:]:
            bllt["x"]+=bllt["dir"][0]*b_spd_cfg;bllt["y"]+=bllt["dir"][1]*b_spd_cfg 
            pygame.draw.circle(frame,module_ORANGE,(int(bllt["x"]),int(bllt["y"])),5) 
            if not(0<bllt["x"]<module_WIDTH and 0<bllt["y"]<module_HEIGHT):bullets_l_ingame.remove(bllt);continue
            b_r=pygame.Rect(bllt["x"]-5,bllt["y"]-5,10,10)
            for e_o in enemies_l_ingame[:]:
                if b_r.colliderect(pygame.Rect(e_o.x,e_o.y,e_o.size,e_o.size)):
                    e_o.hp-=atk_dmg
                    if any(eq["name"]=="Explosive Shotgun" for eq in p_eq_ingame):
                        for o_e in enemies_l_ingame:
                            if math.hypot(o_e.x-e_o.x,o_e.y-e_o.y)<50:o_e.hp-=5
                        add_floating_text_local(floating_texts_l_ingame,"💥Explosion!",(e_o.x,e_o.y))
                    if e_o.hp<=0:drop_equipment_local(e_o,p_eq_ingame);enemies_l_ingame.remove(e_o);p_exp+=25
                    if bllt in bullets_l_ingame:bullets_l_ingame.remove(bllt);break
        enemies_l_ingame[:]=[e for e in enemies_l_ingame if e.hp>0]
        draw_floating_texts_local(frame, floating_texts_l_ingame) 
        draw_hp_bar_local(frame,php,pm_hp)
        draw_exp_bar_local(frame,p_exp,p_lvl)
        draw_game_info_local(frame,p_lvl,_current_wave_module_level,MAX_WAVES_CONFIG)
        draw_equipment_panel_local(frame,p_eq_ingame)
        enemies_txt=module_fonts['upgrade'].render(f"Enemies Left: {len(enemies_l_ingame)+rem_en_spawn}",True,module_BLACK)
        frame.blit(enemies_txt,(module_WIDTH//2-enemies_txt.get_width()//2,20))
        blit_off=(0,0)
        if sshake_end_t>now:blit_off=(random.randint(-sshake_int,sshake_int),random.randint(-sshake_int,sshake_int));sshake_end_t=max(0,sshake_end_t-dt) 
        else: sshake_int=0
        module_screen.blit(frame,blit_off);pygame.display.flip()
        if not enemies_l_ingame and rem_en_spawn==0:
            if _current_wave_module_level>=MAX_WAVES_CONFIG:
                win_s=module_fonts['main'].render("You cleared all waves! VICTORY!",True,module_GREEN);module_screen.blit(win_s,(module_WIDTH//2-win_s.get_width()//2,module_HEIGHT//2-win_s.get_height()//2));pygame.display.flip();pygame.time.delay(3000);running=False
            else:next_wave_local_ingame()
        req_exp_val=30*(p_lvl**2) if p_lvl > 0 else 30
        if p_exp>=req_exp_val:
            p_exp-=req_exp_val;p_lvl+=1;php=pm_hp;is_upg=True;upg_done=False
            elig_opts=[opt for opt in UPGRADE_OPTIONS_DATA if p_lvl>=opt["level_required"]]
            choices=random.sample(elig_opts,min(len(elig_opts),3))
            exec_v={"player_max_hp":pm_hp,"attack_damage":atk_dmg,"base_player_speed":base_spd,
                    "player_hp_regen":php_regen,"player_crit_rate":pc_rate,"player_dodge_rate":pd_rate,
                    "weapons":wpns.copy(),"player_speed":base_spd}
            while is_upg and not upg_done:
                cur_blit_off=blit_off;module_screen.blit(frame,cur_blit_off) 
                draw_upgrade_overlay_local(module_screen,choices,p_lvl)
                pygame.display.flip()
                for evt_u in pygame.event.get():
                    if evt_u.type==pygame.QUIT:running=False;is_upg=False
                if not running:break
                for opt_c in choices:
                    if keyboard.is_pressed(opt_c["key_binding"]):
                        try:
                            exec(opt_c["effect"],{"pygame":pygame,"math":math,"random":random},exec_v)
                            pm_hp=exec_v["player_max_hp"];atk_dmg=exec_v["attack_damage"]
                            base_spd=exec_v.get("player_speed",base_spd);php_regen=exec_v["player_hp_regen"]
                            pc_rate=exec_v["player_crit_rate"];pd_rate=exec_v["player_dodge_rate"]
                            wpns=exec_v["weapons"]
                        except Exception as e:print(f"Error applying upgrade '{opt_c['name']}': {e}")
                        upg_done=True;is_upg=False;break
                pygame.time.wait(20)
            if upg_done:php=pm_hp
        if php<=0:
            restart_c=end_screen_local(game_clock_ref)
            if restart_c:reset_state_local_ingame();next_wave_local_ingame();game_st="playing"
            else:running=False
    pygame.quit();sys.exit()

[end of game/game.py]
