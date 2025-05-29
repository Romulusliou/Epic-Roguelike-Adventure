# game/wave_manager.py
# current_wave = 1
# max_waves = 10
# total_enemies_in_wave = 20
# remaining_enemies_to_spawn = total_enemies_in_wave

# def next_wave():
#     """進入下一波敵人"""
#     global current_wave, remaining_enemies_to_spawn, total_enemies_in_wave
#
#     if current_wave < max_waves:
#         current_wave += 1
#         total_enemies_in_wave += 5  # 每波敵人數量增加
#         remaining_enemies_to_spawn = total_enemies_in_wave
#         print(f"🌊 進入第 {current_wave} 波！")
#     else:
#         print("🎉 恭喜！已通關所有波次！")

# def is_wave_cleared():
#     """檢查是否清光當前波的敵人"""
#     from enemy.enemy import enemies # This import is part of the commented out function
#     return len(enemies) == 0 and remaining_enemies_to_spawn == 0
