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
        
        self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()
        
        self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()
        
        self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()
        
    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index, block in enumerate(self.body):
            x_pos = int(block.x * CELL_SIZE)
            y_pos = int(block.y * CELL_SIZE)
            block_rect = pygame.Rect(x_pos, y_pos, CELL_SIZE, CELL_SIZE)    
            
            if index == 0:
                SCREEN.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                SCREEN.blit(self.tail, block_rect)


class Fruit():
    def __init__(self):
        self.randomise()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * CELL_SIZE), int(self.pos.y * CELL_SIZE), CELL_SIZE, CELL_SIZE)
        SCREEN.blit(apple, fruit_rect)

    def randomise(self):
        self.x = random.randint(0, CELL_NUMBER - 1)
        self.y = random.randint(0, CELL_NUMBER - 1) 
        self.pos = Vector2(self.x, self.y)


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
