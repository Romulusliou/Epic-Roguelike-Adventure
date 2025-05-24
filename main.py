# main.py
import pygame
import sys
from settings.settings import init_settings
from game.game import run_game  # ✅ 確保 `run_game` 存在於 `game.py`

pygame.init()
screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
clock = pygame.time.Clock()

# 遊戲主迴圈
def main():
    run_game(screen, clock)

if __name__ == "__main__":
    main()
