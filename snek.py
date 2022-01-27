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

            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block

                if previous_block.x == next_block.x:
                    SCREEN.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    SCREEN.blit(self.body_horizontal, block_rect)

                else:
                    if (previous_block.x == -1 and next_block.y == -1) or (previous_block.y == -1 and next_block.x == -1):
                        SCREEN.blit(self.body_tl, block_rect)
                    elif (previous_block.x == -1 and next_block.y == 1) or (previous_block.y == 1 and next_block.x == -1):
                        SCREEN.blit(self.body_bl, block_rect)
                    elif (previous_block.x == 1 and next_block.y == -1) or (previous_block.y == -1 and next_block.x == 1):
                        SCREEN.blit(self.body_tr, block_rect)
                    elif (previous_block.x == 1 and next_block.y == 1) or (previous_block.y == 1 and next_block.x == 1):
                        SCREEN.blit(self.body_br, block_rect)                        
            
    def update_head_graphics(self):
        head_body_vector = self.body[1] - self.body[0]
        if head_body_vector == Vector2(1, 0):
            self.head = self.head_left
        elif head_body_vector == Vector2(-1, 0):
            self.head = self.head_right
        elif head_body_vector == Vector2(0, 1):
            self.head = self.head_up
        elif head_body_vector == Vector2(0, -1):
            self.head = self.head_down

    def update_tail_graphics(self):
        tail_body_vector = self.body[-2] - self.body[-1]
        if tail_body_vector == Vector2(1, 0):
            self.tail = self.tail_left
        elif tail_body_vector == Vector2(-1, 0):
            self.tail = self.tail_right
        elif tail_body_vector == Vector2(0, 1):
            self.tail = self.tail_up
        elif tail_body_vector == Vector2(0, -1):
            self.tail = self.tail_down

    def move_snake(self):
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False

        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def play_sound(self):
        self.crunch_sound.play()

    def reset(self):
        self.body = [Vector2(20, 20), Vector2(19, 20), Vector2(18, 20)]
        self.direction = Vector2(0, 0)
        

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

    def update(self):
        self.snake.move_snake()
        self.check_fruit_collision()
        self.check_fail()

    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def check_fruit_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.snake.play_sound()
            self.fruit.randomise()
            self.snake.add_block()
        
        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomise()

    def check_fail(self):
        if not (0 <= self.snake.body[0].x < CELL_NUMBER) or not (0 <= self.snake.body[0].y < CELL_NUMBER):
            self.game_over()
        
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        self.snake.reset()

    def draw_grass(self):
        grass_colour = (167, 209, 61)
        for row in range(CELL_NUMBER):
            if row % 2 == 0:
                for col in range(CELL_NUMBER):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        pygame.draw.rect(SCREEN, grass_colour, grass_rect)
            else:
                for col in range(CELL_NUMBER):
                    if col % 2:
                        grass_rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        pygame.draw.rect(SCREEN, grass_colour, grass_rect)            
        
    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surf = game_font.render(score_text, 1, (0, 0, 0))
        score_x = int(CELL_SIZE * CELL_NUMBER) - 60
        score_y = int(CELL_SIZE * CELL_NUMBER) - 40
        score_rect = score_surf.get_rect(center = (score_x, score_y))
        apple_rect = apple.get_rect(midright = (score_rect.left - 5, score_rect.centery))

        SCREEN.blit(score_surf, score_rect)
        SCREEN.blit(apple, apple_rect)    
            
            
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Main Function

def main():
    timer = 80
    SCREEN_UPDATE = pygame.USEREVENT
    pygame.time.set_timer(SCREEN_UPDATE, timer)

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Constants

pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)
CLOCK = pygame.time.Clock()
CELL_SIZE = 20
CELL_NUMBER = 40
SCREEN_WIDTH = CELL_NUMBER * CELL_SIZE
SCREEN_HEIGHT = CELL_NUMBER * CELL_SIZE
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Snek | Asianguy_123')
main_game = Main()
apple = pygame.image.load('Graphics/apple.png').convert_alpha()
game_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Runs Program

if __name__ == '__main__':
    main()
