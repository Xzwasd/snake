import random
from pygame.math import Vector2
from settings import *
from random import choice

class Snake:
	def __init__(self, blocked_positions=None):
		self.blocked_positions = blocked_positions if blocked_positions else []
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

		directions = [
			Vector2(1, 0),  # вправо
			Vector2(-1, 0),  # влево
			Vector2(0, 1),  # вниз
			Vector2(0, -1)  # вверх
		]

		snake_length = 3
		valid_starts = []

		for x in range(number_of_cells):
			for y in range(number_of_cells):
				head = Vector2(x, y)
				for direction in directions:
					body = [head + direction * i for i in range(snake_length)]

					# Проверка: ни один сегмент тела не должен быть в стене или вне поля
					if all(
							0 <= segment.x < number_of_cells and
							0 <= segment.y < number_of_cells and
							segment not in self.blocked_positions
							for segment in body):
						valid_starts.append((body, direction))

		# Если ничего не подошло
		if not valid_starts:
			raise Exception("Нет подходящих стартовых позиций для змейки. Все заблокированы стенами.")

		# Выбор случайной подходящей позиции
		self.body, self.direction = random.choice(valid_starts)

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