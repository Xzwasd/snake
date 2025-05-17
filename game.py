import pygame
from food import Food
from snake import Snake
from settings import *
import time



class Game:
	def __init__(self):
		self.snake = Snake()
		self.food = Food(self.snake.body)
		self.state = "WAITING"
		self.score = 0
		self.show_start_message = True  # Флаг для показа подсказки один раз

	def draw(self):
		self.food.draw()
		self.snake.draw()

	def update(self):
		if self.state == "RUNNING":
			current_time = time.time()
			# Еда исчезает, если прошло больше 7 секунд
			if current_time - self.food.spawn_time > 7:
				self.food.position = self.food.generate_random_pos(self.snake.body)

			self.snake.update()
			self.check_collision_with_food()
			self.check_collision_with_edges()
			self.check_collision_with_tail()

	def check_collision_with_food(self):
		if self.snake.body[0] == self.food.position:
			self.food.position = self.food.generate_random_pos(self.snake.body)
			self.snake.add_segment = True
			self.score += 1
			#self.snake.eat_sound.play()

	def check_collision_with_edges(self):
		if self.snake.body[0].x == number_of_cells or self.snake.body[0].x == -1:
			self.game_over()
		if self.snake.body[0].y == number_of_cells or self.snake.body[0].y == -1:
			self.game_over()

	def check_collision_with_tail(self):
		headless_body = self.snake.body[1:]
		if self.snake.body[0] in headless_body:
			self.game_over()

	def game_over(self):
		self.snake.reset()
		self.food.position = self.food.generate_random_pos(self.snake.body)
		self.state = "STOPPED"
		self.score = 0
		#self.snake.wall_hit_sound.play()