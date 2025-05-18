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
		self.score_font = pygame.font.Font(None, 40)
		self.pause_font = pygame.font.Font(None, 70)

	def draw(self):
		self.food.draw()
		self.snake.draw()
		if self.state == "WAITING":
			self.draw_start_message()
		if self.state == "PAUSED":
			self.draw_pause_message()

	def draw_start_message(self): #отрисовка подсказки во время ожидания
		start_surface = self.score_font.render("Press key to start", True, DARK_GREEN, GREEN)
		text_rect = start_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
		screen.blit(start_surface, text_rect)

	def draw_pause_message(self): #отрисовка паузы
		start_surface = self.pause_font.render("PAUSE", True, DARK_GREEN, GREEN)
		text_rect = start_surface.get_rect(center=(screen.get_width() // 2 + 30, screen.get_height() // 2 + 30))
		screen.blit(start_surface, text_rect)

	def toggle_pause(self): #пауза
		if self.state == "RUNNING":
			self.state = "PAUSED"
		elif self.state == "PAUSED":
			self.state = "RUNNING"

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
			self.draw_start_message()


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
		self.state = "WAITING"
		self.score = 0
		#self.snake.wall_hit_sound.play()