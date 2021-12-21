import pygame
from game import Game
import variables

game = Game()

running = True
while running:
    # Track all events``
    running = game.events()

    # Show game background
    game.show_background()

    # Update all sprite groups, in 1 line :))
    game.update_group()

    # Detects whether to show the result panel
    game.lose_screen()

    # Show score when the game is active
    game.show_score(variables.score, game.WIDTH / 2, 100, False)
    game.fps()

pygame.quit()
