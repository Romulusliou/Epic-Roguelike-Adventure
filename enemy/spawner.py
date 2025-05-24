# enemy/spawner.py
import random
from enemy.enemy import Enemy, enemies
from game.wave_manager import current_wave, remaining_enemies_to_spawn, is_wave_cleared, next_wave


bombs = []
current_wave = 1
max_waves = 3
wave_interval = 5000
last_wave_time = 0
wave_started = False
wave_enemy_count = 0
enemies_in_wave = 5
enemies_killed_in_wave = 0
boss_wave_mod = 5


wave_enemy_types = {
    1: ["normal"],
    3: ["normal", "elite", "swift"],
    5: ["normal", "elite", "swift", "tank"],
    7: ["normal", "elite", "swift", "tank", "healer"],
    9: ["normal", "elite", "swift", "tank", "healer", "bomber", "summoner"]
}

def spawn_enemy():
    """根據當前波數生成敵人"""
    types = wave_enemy_types.get(current_wave, wave_enemy_types[max(wave_enemy_types.keys())])
    etype = random.choice(types)

    if current_wave == 10 and not any(e.etype == "boss" for e in enemies):
        etype = "boss"

    x = random.randint(100, 800)
    y = random.randint(100, 600)
    enemies.append(Enemy(x, y, etype, current_wave))

def handle_wave_transition():
    """檢查是否進入下一波，並生成敵人"""
    global remaining_enemies_to_spawn

    if is_wave_cleared():
        next_wave()

    while len(enemies) < 5 and remaining_enemies_to_spawn > 0:
        spawn_enemy()
        remaining_enemies_to_spawn -= 1
