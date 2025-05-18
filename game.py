from food import Food
from snake import Snake
from settings import *
import time, sys



class Game:
	def __init__(self):
		self.snake = Snake()
		self.food = Food(self.snake.body)
		self.state = "MENU"
		self.score = 0
		self.score_font = pygame.font.Font(None, 40)
		self.pause_font = pygame.font.Font(None, 70)

	def draw(self):
		if self.state == 'MENU':
			self.draw_menu()
		else:
			self.food.draw()
			self.snake.draw()
			if self.state == "WAITING": #Начальное сообщение
				self.draw_start_message()
			if self.state == "PAUSED": #Пауза
				self.draw_pause_message()

	def draw_menu(self):
		surface = pygame.display.get_surface()
		width, height = surface.get_size()
		surface.fill(GREEN)

		title_font = pygame.font.Font(None, 64)
		button_font = pygame.font.Font(None, 36)

		# Заголовок
		title_text = title_font.render("SNAKE", True, (0, 255, 0))
		title_rect = title_text.get_rect(center=(width // 2, height // 4))
		surface.blit(title_text, title_rect)

		# Кнопка "Start Game"
		button_width, button_height = 200, 60
		start_x = (width - button_width) // 2
		start_y = height // 2
		self.start_button_rect = pygame.Rect(start_x, start_y, button_width, button_height)
		pygame.draw.rect(surface, (0, 100, 0), self.start_button_rect)
		start_text = button_font.render("Start Game", True, (255, 255, 255))
		start_rect = start_text.get_rect(center=self.start_button_rect.center)
		surface.blit(start_text, start_rect)

		# Кнопка "Exit"
		exit_y = start_y + button_height + 30  # отступ 30px между кнопками
		self.exit_button_rect = pygame.Rect(start_x, exit_y, button_width, button_height)
		pygame.draw.rect(surface, (100, 0, 0), self.exit_button_rect)
		exit_text = button_font.render("Exit", True, (255, 255, 255))
		exit_rect = exit_text.get_rect(center=self.exit_button_rect.center)
		surface.blit(exit_text, exit_rect)

	def handle_menu_input(self, pos):
		if self.start_button_rect.collidepoint(pos):
			self.state = "WAITING"
		elif self.exit_button_rect.collidepoint(pos):
			pygame.quit()
			sys.exit()

	def draw_start_message(self): #отрисовка подсказки во время ожидания
		start_surface = self.score_font.render("Press key to start", True, DARK_GREEN)
		text_rect = start_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
		screen.blit(start_surface, text_rect)

	def draw_pause_message(self): #отрисовка паузы
		surface = pygame.display.get_surface()
		#Затемнение
		dark_overlay = pygame.Surface(surface.get_size())
		dark_overlay.set_alpha(40)  #Прозрачность
		dark_overlay.fill((0, 0, 0))
		surface.blit(dark_overlay, (0, 0))
		#Пауза
		text = self.pause_font.render("PAUSE", True, DARK_GREEN)
		text_rect = text.get_rect(center=(screen.get_width() // 2 + 30, screen.get_height() // 2 + 30))
		screen.blit(text, text_rect)

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