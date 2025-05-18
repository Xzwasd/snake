from food import Food
from snake import Snake
from settings import *
import time, sys, json, os



class Game:
	def __init__(self):
		self.snake = Snake()
		self.food = Food(self.snake.body)
		self.state = "MENU"
		self.score = 0
		self.max_score = self.load_max_score()
		self.continue_button_rect = pygame.Rect(0, 0, 250, 80)
		self.menu_button_rect = pygame.Rect(0, 0, 250, 80)
		self.score_font = pygame.font.Font("assets/alagard-12px-unicode.ttf", 64)
		self.pause_font = pygame.font.Font("assets/alagard-12px-unicode.ttf", 64)
		self.button_font = pygame.font.Font("assets/alagard-12px-unicode.ttf", 32)
		self.title_font = pygame.font.Font("assets/alagard-12px-unicode.ttf", 64)
		self.menu_background = pygame.image.load("assets/menu_bg.png").convert()
		self.button = pygame.image.load("assets/button_bg.png").convert()

		# Мигание подсказки
		self.show_start_message = True
		self.last_toggle_time = time.time()
		self.blink_interval = 0.7

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

		# --- Фон меню ---
		bg = pygame.image.load("assets/menu_bg.png").convert()
		bg = pygame.transform.scale(bg, (width, height))
		surface.blit(bg, (0, 0))

		# --- Максимальный счет ---
		high_score_text = self.button_font.render(f"High Score: {self.max_score}", True, (255, 255, 255))
		high_score_rect = high_score_text.get_rect(center=(width // 2, height // 2 - 80))
		screen.blit(high_score_text, high_score_rect)

		# --- Название игры ---
		title_text = self.title_font.render("SNAKE", True, (255, 255, 255))
		title_rect = title_text.get_rect(center=(width // 2, height // 5))
		surface.blit(title_text, title_rect)

		# --- Кнопки с изображениями ---
		# Загрузка и масштабирование картинок
		start_img_raw = pygame.image.load("assets/button_bg.png").convert_alpha()
		exit_img_raw = pygame.image.load("assets/button_bg.png").convert_alpha()
		button_size = (250, 80)

		self.start_img = pygame.transform.scale(start_img_raw, button_size)
		self.exit_img = pygame.transform.scale(exit_img_raw, button_size)

		# Позиции кнопок
		start_pos = (width // 2 - button_size[0] // 2, height // 2)
		exit_pos = (width // 2 - button_size[0] // 2, height // 2 + button_size[1] + 30)

		self.start_button_rect = pygame.Rect(start_pos, button_size)
		self.exit_button_rect = pygame.Rect(exit_pos, button_size)

		# --- Отрисовка кнопок ---
		# Start
		surface.blit(self.start_img, self.start_button_rect)
		start_text = self.button_font.render("Start Game", True, (255, 255, 255))
		start_text_rect = start_text.get_rect(center=self.start_button_rect.center)
		surface.blit(start_text, start_text_rect)

		# Exit
		surface.blit(self.exit_img, self.exit_button_rect)
		exit_text = self.button_font.render("Exit", True, (255, 255, 255))
		exit_text_rect = exit_text.get_rect(center=self.exit_button_rect.center)
		surface.blit(exit_text, exit_text_rect)

	def handle_menu_input(self, pos):
		if self.start_button_rect.collidepoint(pos):
			self.reset()
		elif self.exit_button_rect.collidepoint(pos):
			pygame.quit()
			sys.exit()

	def draw_start_message(self):
		if self.show_start_message:
			start_surface = self.score_font.render("Press key to start", True, DARK_GREEN, GREEN)
			text_rect = start_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
			screen.blit(start_surface, text_rect)

	def draw_pause_message(self): #отрисовка паузы
		surface = pygame.display.get_surface()
		width, height = surface.get_size()
		self.continue_img = pygame.transform.scale(
			pygame.image.load("assets/button_bg.png").convert_alpha(), (250, 80)
		)
		self.menu_img = pygame.transform.scale(
			pygame.image.load("assets/button_bg.png").convert_alpha(), (250, 80)
		)
		# --- Затемнение ---
		dark_overlay = pygame.Surface((width, height))
		dark_overlay.set_alpha(40)
		dark_overlay.fill((0, 0, 0))
		surface.blit(dark_overlay, (0, 0))

		# --- Текст "PAUSE" ---
		text = self.pause_font.render("PAUSE", True, DARK_GREEN)
		text_rect = text.get_rect(center=(width // 2, height // 2 - 100))
		surface.blit(text, text_rect)

		# --- Кнопки ---
		button_gap = 30

		# 1. Continue
		self.continue_button_rect.center = (width // 2, height // 2)
		surface.blit(self.continue_img, self.continue_button_rect)
		continue_text = self.button_font.render("Continue", True, (255, 255, 255))
		continue_text_rect = continue_text.get_rect(center=self.continue_button_rect.center)
		surface.blit(continue_text, continue_text_rect)

		# 2. Back to Menu
		self.menu_button_rect.center = (width // 2, height // 2 + 80 + button_gap)
		surface.blit(self.menu_img, self.menu_button_rect)
		menu_text = self.button_font.render("Back to Menu", True, (255, 255, 255))
		menu_text_rect = menu_text.get_rect(center=self.menu_button_rect.center)
		surface.blit(menu_text, menu_text_rect)

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
		if self.score > self.max_score:
			self.max_score = self.score
			self.save_max_score()
		self.snake.reset()
		self.food.position = self.food.generate_random_pos(self.snake.body)
		self.state = "WAITING"
		self.score = 0
		#self.snake.wall_hit_sound.play()

	def reset(self): #новая игра
		self.snake = Snake()
		self.food = Food(self.snake.body)
		self.score = 0
		self.state = "WAITING"

	def load_max_score(self):
		path = "data/max_score.json"
		if not os.path.exists(path):
			with open(path, "w") as f:
				json.dump({"max_score": 0}, f)
			return 0
		with open(path, "r") as f:
			data = json.load(f)
			return data.get("max_score", 0)

	def save_max_score(self):
		path = "data/max_score.json"
		with open(path, "w") as f:
			json.dump({"max_score": self.max_score}, f)