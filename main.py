# main.py
import pygame
import sys
# Import init_settings from the settings module
from settings.settings import init_settings
# Import the Game class
from game.game import Game

def main():
    pygame.init()

    # Load settings
    WIDTH, HEIGHT, font, equip_font, upgrade_font, upgrade_font_small = init_settings()

    # Set up the display
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("穿越成為成最強冒險家") # (Keeping original title for now)

    # Clock for managing FPS
    clock = pygame.time.Clock()

    # Instantiate the Game class
    game_instance = Game(screen, WIDTH, HEIGHT, font)

    running = True
    while running:
        # Calculate delta time
        dt = clock.tick(60) / 1000.0

        # Get events once per frame
        events = pygame.event.get() 

        # Still need this loop in main.py to catch QUIT and ESCAPE for global exit
        for event in events: 
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        if not running: # Exit loop immediately if running is set to False by event handling
            break
            
        # Run the game iteration
        game_instance.run_iteration(dt, events)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
