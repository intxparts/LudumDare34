import pygame
from Game.Framework.Scene import *


class GameScene(Scene):
    
    def __init__(self, screen_dimensions):
        super(GameScene, self).__init__(screen_dimensions)

    def reset(self):
        pass

    def update(self, events):
        # handle input
        for event in events:
            # handle clicking the X on the game window
            if event.type == pygame.QUIT:
                return 'exit'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # return exit to trigger graceful exit of program
                    return 'exit'

    def draw(self, display):
        black = (0, 0, 0)
        display.fill(black)

    def id(self):
        return 'game_scene'
