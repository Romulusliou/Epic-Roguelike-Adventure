# game/game.py
import pygame
import sys
from settings import settings  # ✅ 確保 settings 模組存在
from ui.ui import draw_floating_texts, draw_pause_menu  # ✅ 確保 ui.ui 模組存在
from ui.menus import end_screen  # ✅ 確保 ui.menus 模組存在 (將 end_screen import 移到頂部)
from character.character import player  # ✅ 確保 character.character 模組存在 (假設 player 物件已在 character/character.py 中正確建立)
from combat.combat import handle_attacks  # ✅ 確保 combat.combat 模組存在
from enemy.enemy import update_enemies  # ✅ 確保 enemy.enemy 模組存在
from enemy.spawner import handle_wave_transition  # ✅ 確保 enemy.spawner 模組存在
from game.effects import apply_screen_shake  # ✅ 確保 game.effects 模組存在
import game.input_handler as input_handler  # ✅ 這樣避免 Python 在載入 `input_handler.py` 時發生循環
from game.effects import trigger_screen_shake, trigger_muzzle_flash, trigger_explosion, update_effects, draw_effects  # ✅ 確保 game.effects 模組存在

print("game/game.py: Code replaced successfully!")  # <<<=== 務必新增 Debug 輸出語句，驗證程式碼替換是否成功！！！

game_state = {  # <<<=== 初始化 game_state 字典 (在檔案頂部定義，成為全局變數)
    'enemies': [],  # ✅ enemies 列表儲存在 game_state 中
    'game_paused': False,  # ✅ 新增遊戲暫停狀態
    # ... (未來可以加入其他遊戲狀態，例如玩家狀態、遊戲設定等等) ...
}

# 在遊戲迴圈外初始化特效 (只執行一次)
update_effects()  # ✅ update_effects() 函數 (假設已正確定義)

def run_game(screen, clock):
    """執行遊戲核心邏輯"""
    running = True
    # game_state = "playing"  # <<<=== 移除 run_game 函數內部的 game_state 字串變數 (改用全局 game_state 字典)

    while running:
        dt = clock.tick(60)
        screen.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            input_handler.handle_input()  # <<<=== 修改：傳入 game_state 給 handle_input()
            handle_attacks(player, game_state['enemies'], event)  # <<<=== 修改：傳入 player 和 game_state['enemies'] 和 event 給 handle_attacks()

        if game_state['game_paused']:  # <<<=== 使用 game_state['game_paused'] 判斷遊戲是否暫停
            draw_pause_menu(screen)
            pygame.display.flip()
            continue  # <<<=== 如果遊戲暫停，跳過後續遊戲邏輯，直接繪製暫停選單

        # 更新遊戲狀態
        handle_wave_transition(game_state['enemies'])  # <<<=== 修改：傳入 game_state['enemies'] 給 handle_wave_transition()
        update_enemies(game_state['enemies'], player)  # <<<=== 修改：傳入 game_state['enemies'] 和 player 給 update_enemies()
        apply_screen_shake(screen)
        draw_floating_texts(screen)

        # 在畫面更新前繪製特效 (移到遊戲迴圈內，每幀執行)
        update_effects()  # ✅ 在遊戲迴圈內更新特效 (每幀執行)
        draw_effects(screen, player.x, player.y)  # ✅ 在畫面更新前繪製特效 (每幀執行)

        pygame.display.update()

        # 玩家死亡檢查
        if player.hp <= 0:
            # from ui.menus import end_screen  # <<<=== 移除此處的局部 import，已移到檔案頂部
            if not end_screen():
                pygame.quit()
                sys.exit()
            else:
                player.reset()
                game_state['enemies'].clear()  # <<<=== 玩家重生時，清空 enemies 列表，重新開始遊戲


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    run_game(screen, clock)