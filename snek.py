# Snek

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Imports

import sys
import pygame
import random
from pygame.math import Vector2

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Classes

class Snake():
    def __init__(self):
        self.body = [Vector2(20, 20), Vector2(19, 20), Vector2(18, 20)]
        self.direction = Vector2(0, 0)
        self.new_block = False
        self.crunch_sound = pygame.mixer.Sound('Sound/crunch.wav')


class Fruit():
    def __init__(self):
        self.randomise()


class Main():
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Main Function

def main():
    pass

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Constants

pygame.init()
CLOCK = pygame.time.Clock()
CELL_SIZE = 20
CELL_NUMBER = 40
SCREEN_WIDTH = CELL_NUMBER * CELL_SIZE
SCREEN_HEIGHT = CELL_NUMBER * CELL_SIZE
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Runs Program

if __name__ == '__main__':
    main()
