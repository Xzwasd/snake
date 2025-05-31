import random
from pygame.math import Vector2
import time
from settings import *


class Food:
    def __init__(self, snake_body, wall_blocks=[]):
        self.wall_blocks = wall_blocks
        self.position = self.generate_random_pos(snake_body)
        self.spawn_game_time = 0  # Время появления еды в игровом времени

    def draw(self):
        food_rect = pygame.Rect(OFFSET + self.position.x * cell_size, OFFSET + self.position.y * cell_size,
            cell_size, cell_size)
        self.food_ige = pygame.transform.scale(food_image, (28, 28))
        screen.blit(self.food_ige, food_rect)

    def generate_random_cell(self):
        x = random.randint(0, number_of_cells-1)
        y = random.randint(0, number_of_cells-1)
        return Vector2(x, y)

    def generate_random_pos(self, snake_body):
        position = self.generate_random_cell()
        while position in snake_body or position in self.wall_blocks:
            position = self.generate_random_cell()
        self.spawn_time = time.time() # Сброс таймера при новом размещении еды
        return position

    def respawn(self, snake_body, current_game_time):
        self.position = self.generate_random_pos(snake_body)
        self.spawn_game_time = current_game_time  # Обновляем таймер в игровом времени


class BigFood(Food):
    def __init__(self, snake_body, wall_blocks=[]):
        super().__init__(snake_body, wall_blocks)
        self.food_image = pygame.transform.scale(big_food_image, (28, 28))  # картинка для BigFood

    def draw(self):
        food_rect = pygame.Rect(
            OFFSET + self.position.x * cell_size,
            OFFSET + self.position.y * cell_size,
            cell_size, cell_size
        )
        screen.blit(self.food_image, food_rect)


class PoisonFood(Food):
    def __init__(self, snake_body, wall_blocks=[]):
        super().__init__(snake_body, wall_blocks)
        self.food_image = pygame.transform.scale(pygame.image.load("assets/images/poison_food.png"), (28, 28))

    def draw(self):
        food_rect = pygame.Rect(
            OFFSET + self.position.x * cell_size,
            OFFSET + self.position.y * cell_size,
            cell_size, cell_size
        )
        screen.blit(self.food_image, food_rect)


class ReversedFood(Food):
    def __init__(self, snake_body, wall_blocks=[]):
        super().__init__(snake_body, wall_blocks)
        self.food_image = pygame.transform.scale(pygame.image.load("assets/images/reversed_food.png"), (28, 28))

    def draw(self):
        food_rect = pygame.Rect(
            OFFSET + self.position.x * cell_size,
            OFFSET + self.position.y * cell_size,
            cell_size, cell_size
        )
        screen.blit(self.food_image, food_rect)
