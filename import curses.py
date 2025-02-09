import curses
import random

# 遊戲設定
MAP_WIDTH = 40
MAP_HEIGHT = 20
PLAYER_CHAR = "@"
ENEMY_CHAR = "E"
WALL_CHAR = "#"
FLOOR_CHAR = "."
ITEM_CHAR = "$"
EXIT_CHAR = ">"
PLAYER_HP = 10
ENEMY_HP = 3
ATTACK_DAMAGE = 2

# 初始化遊戲
def init_game():
    # 創建地圖
    game_map = [[WALL_CHAR if x == 0 or x == MAP_WIDTH - 1 or y == 0 or y == MAP_HEIGHT - 1 else FLOOR_CHAR for x in range(MAP_WIDTH)] for y in range(MAP_HEIGHT)]
    # 放置玩家
    player_x, player_y = random.randint(1, MAP_WIDTH - 2), random.randint(1, MAP_HEIGHT - 2)
    game_map[player_y][player_x] = PLAYER_CHAR
    # 放置敵人
    enemy_x, enemy_y = random.randint(1, MAP_WIDTH - 2), random.randint(1, MAP_HEIGHT - 2)
    while (enemy_x, enemy_y) == (player_x, player_y):
        enemy_x, enemy_y = random.randint(1, MAP_WIDTH - 2), random.randint(1, MAP_HEIGHT - 2)
    game_map[enemy_y][enemy_x] = ENEMY_CHAR
    # 放置出口
    exit_x, exit_y = random.randint(1, MAP_WIDTH - 2), random.randint(1, MAP_HEIGHT - 2)
    while (exit_x, exit_y) == (player_x, player_y) or (exit_x, exit_y) == (enemy_x, enemy_y):
        exit_x, exit_y = random.randint(1, MAP_WIDTH - 2), random.randint(1, MAP_HEIGHT - 2)
    game_map[exit_y][exit_x] = EXIT_CHAR
    return game_map, player_x, player_y, enemy_x, enemy_y, exit_x, exit_y, PLAYER_HP, ENEMY_HP

# 主遊戲循環
def main(stdscr):
    curses.curs_set(0)  # 隱藏游標
    stdscr.nodelay(1)   # 非阻塞輸入
    stdscr.timeout(100) # 每100ms更新一次

    game_map, player_x, player_y, enemy_x, enemy_y, exit_x, exit_y, player_hp, enemy_hp = init_game()

    while True:
        stdscr.clear()
        # 繪製地圖
        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                stdscr.addch(y, x, game_map[y][x])
        # 顯示玩家血量
        stdscr.addstr(MAP_HEIGHT + 1, 0, f"HP: {player_hp}")
        # 處理輸入
        key = stdscr.getch()
        new_x, new_y = player_x, player_y
        if key == curses.KEY_UP and player_y > 1:
            new_y -= 1
        elif key == curses.KEY_DOWN and player_y < MAP_HEIGHT - 2:
            new_y += 1
        elif key == curses.KEY_LEFT and player_x > 1:
            new_x -= 1
        elif key == curses.KEY_RIGHT and player_x < MAP_WIDTH - 2:
            new_x += 1
        # 檢查移動是否合法
        if game_map[new_y][new_x] == FLOOR_CHAR or game_map[new_y][new_x] == EXIT_CHAR:
            game_map[player_y][player_x] = FLOOR_CHAR
            player_x, player_y = new_x, new_y
            game_map[player_y][player_x] = PLAYER_CHAR
        # 檢查是否遇到敵人
        if (player_x, player_y) == (enemy_x, enemy_y):
            enemy_hp -= ATTACK_DAMAGE
            if enemy_hp <= 0:
                game_map[enemy_y][enemy_x] = FLOOR_CHAR
                stdscr.addstr(MAP_HEIGHT + 2, 0, "你擊敗了敵人！")
            else:
                player_hp -= 1
                stdscr.addstr(MAP_HEIGHT + 2, 0, f"你受到攻擊！剩餘HP: {player_hp}")
        # 檢查是否到達出口
        if (player_x, player_y) == (exit_x, exit_y):
            stdscr.addstr(MAP_HEIGHT + 2, 0, "你找到了出口！遊戲勝利！")
            break
        # 檢查玩家是否死亡
        if player_hp <= 0:
            stdscr.addstr(MAP_HEIGHT + 2, 0, "你死了！遊戲結束！")
            break
        stdscr.refresh()

# 啟動遊戲
if __name__ == "__main__":
    curses.wrapper(main)