import pygame, sys, random
from pygame.math import Vector2
from settings import *
from random import choice

class Snake:
	def __init__(self):
		self.reset()
		#self.eat_sound = pygame.mixer.Sound("Sounds/eat.mp3")
		#self.wall_hit_sound = pygame.mixer.Sound("Sounds/wall.mp3")

	def draw(self):
		for segment in self.body:
			segment_rect = (OFFSET + segment.x * cell_size, OFFSET+ segment.y * cell_size, cell_size, cell_size)
			pygame.draw.rect(screen, DARK_GREEN, segment_rect, 0, 7)

	def update(self):
		self.body.insert(0, self.body[0] + self.direction)
		if self.add_segment:
			self.add_segment = False
		else:
			self.body = self.body[:-1]

	def reset(self):
		self.add_segment = False

		# Возможные направления: вправо, влево, вниз, вверх
		directions = [
			Vector2(1, 0),
			Vector2(-1, 0),
			Vector2(0, 1),
			Vector2(0, -1)
		]

		self.direction = choice(directions)

		# Размер тела змейки
		snake_length = 3

		# Расчёт допустимых координат головы в зависимости от направления
		if self.direction == Vector2(1, 0):  # вправо
			x = random.randint(2, number_of_cells - 1)
			y = random.randint(0, number_of_cells - 1)
			self.body = [Vector2(x - i, y) for i in range(snake_length)]

		elif self.direction == Vector2(-1, 0):  # влево
			x = random.randint(0, number_of_cells - 3)
			y = random.randint(0, number_of_cells - 1)
			self.body = [Vector2(x + i, y) for i in range(snake_length)]

		elif self.direction == Vector2(0, 1):  # вниз
			x = random.randint(0, number_of_cells - 1)
			y = random.randint(2, number_of_cells - 1)
			self.body = [Vector2(x, y - i) for i in range(snake_length)]

		elif self.direction == Vector2(0, -1):  # вверх
			x = random.randint(0, number_of_cells - 1)
			y = random.randint(0, number_of_cells - 3)
			self.body = [Vector2(x, y + i) for i in range(snake_length)]