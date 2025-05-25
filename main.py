# main.py
import pygame
import sys
from settings.settings import init_settings
from game.game import run_game  # ✅ 確保 `run_game` 存在於 `game.py`

pygame.init()
clock = pygame.time.Clock()

# 遊戲主迴圈
def main():
    settings_dict = init_settings()
    run_game(settings_dict, clock)

if __name__ == "__main__":
    main()
