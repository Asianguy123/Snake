# Snek

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Imports

import sys
import pygame
import random
from pygame.math import Vector2 # easier to manipulate and use than lists

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Classes

class Snake():

    '''
    SNAKE CLASS:

    - Creates snake
    - Handles output and image sorting
    - Snake movement
    - Snake growth
    - Snake reset
    '''

    def __init__(self):
        '''
        Initiates snake object with:
        
        - all required images
        - an initial 3 block body (with head at centre facing right)
        - an initial direction of 0
        '''

        # snake inital build
        self.body = [Vector2(20, 20), Vector2(19, 20), Vector2(18, 20)]
        self.direction = Vector2(0, 0)
        self.new_block = False
        self.crunch_sound = pygame.mixer.Sound('Sound/crunch.wav')

        # snake head images
        self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()

        # snake tail images
        self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()

        # snake body, and turning images
        self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()
        self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()

    def draw_snake(self):
        '''
        Outputs required snake images, updates head, tail and turning images
        '''

        # snake head and tail update checks
        self.update_head_graphics()
        self.update_tail_graphics()

        # loops through snake body list to get index and vector
        for index, block in enumerate(self.body):
            # assigns position on grid and creates block rectangle for display
            x_pos = int(block.x * CELL_SIZE)
            y_pos = int(block.y * CELL_SIZE)
            block_rect = pygame.Rect(x_pos, y_pos, CELL_SIZE, CELL_SIZE)

            # checks if block is head or tail - outputs if so
            if index == 0:
                SCREEN.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                SCREEN.blit(self.tail, block_rect)

            else:
                # gets previous and next block in body
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block

                # check to see if in straight line, if so outputs vertical/horizontal image
                if previous_block.x == next_block.x:
                    SCREEN.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    SCREEN.blit(self.body_horizontal, block_rect)

                else:
                    # checks for turns based on vector directions of blocks, outputs appropriate image
                    if (previous_block.x == -1 and next_block.y == -1) or (previous_block.y == -1 and next_block.x == -1):
                        SCREEN.blit(self.body_tl, block_rect)
                    elif (previous_block.x == -1 and next_block.y == 1) or (previous_block.y == 1 and next_block.x == -1):
                        SCREEN.blit(self.body_bl, block_rect)
                    elif (previous_block.x == 1 and next_block.y == -1) or (previous_block.y == -1 and next_block.x == 1):
                        SCREEN.blit(self.body_tr, block_rect)
                    elif (previous_block.x == 1 and next_block.y == 1) or (previous_block.y == 1 and next_block.x == 1):
                        SCREEN.blit(self.body_br, block_rect)                        
            
    def update_head_graphics(self):
        '''
        Checks direction of travel of snake, then assigns necessary head image
        '''

        head_body_vector = self.body[1] - self.body[0] # getting vector of head direction
        if head_body_vector == Vector2(1, 0):
            self.head = self.head_left
        elif head_body_vector == Vector2(-1, 0):
            self.head = self.head_right
        elif head_body_vector == Vector2(0, 1):
            self.head = self.head_up
        elif head_body_vector == Vector2(0, -1):
            self.head = self.head_down

    def update_tail_graphics(self):
        '''
        Checks direction of travel of tail, then assigns necessary tail image
        '''

        tail_body_vector = self.body[-2] - self.body[-1] # getting vector of tail direction
        if tail_body_vector == Vector2(1, 0):
            self.tail = self.tail_left
        elif tail_body_vector == Vector2(-1, 0):
            self.tail = self.tail_right
        elif tail_body_vector == Vector2(0, 1):
            self.tail = self.tail_up
        elif tail_body_vector == Vector2(0, -1):
            self.tail = self.tail_down

    def move_snake(self):
        '''
        Moves snake in direction of vector, or adds new block when fruit is consumed
        '''

        # checks if new block is needed, if yes then copies body and adds extra block
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        
        else:
            # copies all blocks except last, adds block in new position to give illusion of movement
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        '''
        Signals that a fruit has been eaten and that the snake must increase in size
        '''

        self.new_block = True

    def play_sound(self):
        '''
        Outputs crunch noise when fruit has been eaten
        '''

        self.crunch_sound.play()

    def reset(self):
        '''
        Sets snake back to 3 blocks, and at default position on grid with no direction
        '''

        self.body = [Vector2(20, 20), Vector2(19, 20), Vector2(18, 20)]
        self.direction = Vector2(0, 0)
        

class Fruit():

    '''
    FRUIT CLASS:

    - Displays fruit
    - Gives fruit random position on grid
    '''

    def __init__(self):
        '''
        Initiates fruit object with a random grid position
        '''

        self.randomise()

    def draw_fruit(self):
        '''
        Makes fruit object rect and outputs to position
        '''

        fruit_rect = pygame.Rect(int(self.pos.x * CELL_SIZE), int(self.pos.y * CELL_SIZE), CELL_SIZE, CELL_SIZE)
        SCREEN.blit(apple, fruit_rect)

    def randomise(self):
        '''
        Assigns random x and y value, stores as position vector
        '''

        self.x = random.randint(0, CELL_NUMBER - 1)
        self.y = random.randint(0, CELL_NUMBER - 1) 
        self.pos = Vector2(self.x, self.y)


class Main():

    '''
    MAIN CLASS:

    - Manages all game logic
    - Controls all game updates
    - Outputs main game
    - Checks for game over conditions
    '''

    def __init__(self):
        '''
        Initiates main object, with snake and fruit as properties
        '''

        self.snake = Snake()
        self.fruit = Fruit()

    def update(self):
        '''
        Game updates:
        
        - moves snake
        - checks for fruit eaten
        - checks if game lost
        '''

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

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == SCREEN_UPDATE:
                main_game.update()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if main_game.snake.direction.y != 1:
                        main_game.snake.direction = Vector2(0, -1)

                if event.key == pygame.K_DOWN:
                    if main_game.snake.direction.y != -1:
                        main_game.snake.direction = Vector2(0, 1)

                if event.key == pygame.K_RIGHT:
                    if main_game.snake.direction.x != -1:
                        main_game.snake.direction = Vector2(1, 0)

                if event.key == pygame.K_LEFT:
                    if main_game.snake.direction.x != 1:
                        main_game.snake.direction = Vector2(-1, 0)
                
        SCREEN.fill((175, 215, 70))
        main_game.draw_elements()
        pygame.display.update()
        CLOCK.tick(60)

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
