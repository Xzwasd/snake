import random
from pygame.math import Vector2
from settings import *
from random import choice

class Snake:
	def __init__(self):
		self.reset()
		self.direction_changed = False
		self.head_image = pygame.image.load("assets/images/snake_head.png").convert_alpha()
		self.body_image = pygame.image.load("assets/images/snake_body.png").convert_alpha()

		# подгон по размеру клетки
		self.head_image = pygame.transform.scale(self.head_image, (cell_size, cell_size))
		self.body_image = pygame.transform.scale(self.body_image, (cell_size, cell_size))

	def draw(self):
		head = self.body[0]
		pos = (OFFSET + head.x * cell_size, OFFSET + head.y * cell_size)

		angle = 0
		if self.direction == Vector2(1, 0):  # вправо
			angle = 0
		elif self.direction == Vector2(0, -1):  # вверх
			angle = 90
		elif self.direction == Vector2(-1, 0):  # влево
			angle = 180
		elif self.direction == Vector2(0, 1):  # вниз
			angle = 270

		head_img_rotated = pygame.transform.rotate(self.head_image, angle)
		screen.blit(head_img_rotated, pos)

		# отрисовка тела
		for segment in self.body[1:]:
			pos = (OFFSET + segment.x * cell_size, OFFSET + segment.y * cell_size)
			screen.blit(self.body_image, pos)

	def update(self):
		self.body.insert(0, self.body[0] + self.direction)
		if isinstance(self.add_segment, int) and self.add_segment > 0:
			self.add_segment -= 1
		else:
			self.body = self.body[:-1]
		self.direction_changed = False

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