import pygame


food_image = pygame.image.load("assets/food.png")
food_speed_image = pygame.image.load("assets/Sprite-yellow.png")

GREEN = (173, 204, 96)
DARK_GREEN = (43, 51, 24)

cell_size = 30
number_of_cells = 25

OFFSET = 75
screen = pygame.display.set_mode((2*OFFSET + cell_size*number_of_cells, 2*OFFSET + cell_size*number_of_cells))