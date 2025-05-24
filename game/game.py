# game/game.py
import pygame

class Game:
    def __init__(self, screen, width, height, font):
        self.screen = screen
        self.width = width
        self.height = height
        self.font = font
        self.game_state = "menu"
        self.score = 0
        self.current_wave = 0
        print("Game class initialized.")

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    if self.game_state == "playing":
                        self.game_state = "paused"
                        print("Game Paused")
                    elif self.game_state == "paused":
                        self.game_state = "playing"
                        print("Game Resumed")

    def update(self, dt):
        if self.game_state == "playing":
            pass

    def render(self):
        if self.game_state == "playing":
            self.screen.fill((30, 30, 30))
            if self.font:
                text = f"State: Playing | Wave: {self.current_wave} | Score: {self.score}"
                playing_text = self.font.render(text, True, (200, 200, 200))
                self.screen.blit(playing_text, (10, 10))
        elif self.game_state == "paused":
            self.screen.fill((60, 60, 60))
            if self.font:
                paused_text = self.font.render("State: Paused. Press P to resume.", True, (200, 200, 200))
                text_rect = paused_text.get_rect(center=(self.width / 2, self.height / 2))
                self.screen.blit(paused_text, text_rect)
        elif self.game_state == "menu":
            self.screen.fill((40, 40, 40))
            if self.font:
                menu_text = self.font.render("State: Menu. (Implement menu options)", True, (200, 200, 200))
                text_rect = menu_text.get_rect(center=(self.width / 2, self.height / 2))
                self.screen.blit(menu_text, text_rect)
        
    def run_iteration(self, dt, events):
        self.handle_events(events)
        self.update(dt)
        self.render()
