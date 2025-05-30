import pygame

font = 'assets/fonts/alagard-12px-unicode.ttf'
food_image = pygame.image.load("assets/images/apple.png")
big_food_image = pygame.image.load("assets/images/speed_food.png")

#snake_title = pygame.image.load


GREEN = (173, 204, 96)
DARK_GREEN = (43, 51, 24)

cell_size = 30
number_of_cells = 25

OFFSET = 75
screen = pygame.display.set_mode((2*OFFSET + cell_size*number_of_cells, 2*OFFSET + cell_size*number_of_cells))