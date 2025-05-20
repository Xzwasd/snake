import pygame

class UI:
	def __init__(self, game):
		self.game = game
		self.screen = pygame.display.get_surface()
		surface = self.screen
		width, height = surface.get_size()

		# --- Шрифты ---
		self.score_font = pygame.font.Font("assets/fonts/alagard-12px-unicode.ttf", 64)
		self.pause_font = pygame.font.Font("assets/fonts/alagard-12px-unicode.ttf", 64)
		self.button_font = pygame.font.Font("assets/fonts/alagard-12px-unicode.ttf", 32)
		self.title_font = pygame.font.Font("assets/fonts/alagard-12px-unicode.ttf", 64)

		# --- Изображения ---
		self.menu_background = pygame.image.load("assets/images/menu_bg.png").convert()
		self.button_bg = pygame.image.load("assets/images/button_bg.png").convert_alpha()

		# --- Кнопки (позиции устанавливаются позже в draw_menu и draw_pause) ---
		self.start_img = pygame.transform.scale(self.button_bg, (250, 80))
		self.exit_img = pygame.transform.scale(self.button_bg, (250, 80))
		self.continue_img = pygame.transform.scale(self.button_bg, (250, 80))
		self.menu_img = pygame.transform.scale(self.button_bg, (250, 80))

		# --- Прямоугольники кнопок (обновляются в draw_... методах) ---
		self.start_button_rect = pygame.Rect(0, 0, 250, 80)
		self.exit_button_rect = pygame.Rect(0, 0, 250, 80)
		self.continue_button_rect = pygame.Rect(0, 0, 250, 80)
		self.menu_button_rect = pygame.Rect(0, 0, 250, 80)

		self.vol_size = (32, 32)
		self.vol_img_inactive = pygame.image.load("assets/images/volume_inactive.png").convert_alpha()
		self.vol_img_active = pygame.image.load("assets/images/volume_active.png").convert_alpha()
		self.vol_img_inactive = pygame.transform.scale(self.vol_img_inactive, self.vol_size)
		self.vol_img_active = pygame.transform.scale(self.vol_img_active, self.vol_size)
		# --- Громкость ---
		self.music_volume = 5
		spacing = 8
		total_width = 10 * self.vol_size[0] + 9 * spacing
		start_x = width // 2 - total_width // 2
		y_pos = height - 200 + 32 + 10
		self.volume_rects = [
			pygame.Rect(start_x + i * (self.vol_size[0] + spacing), y_pos, *self.vol_size)
			for i in range(10)
		]


		# --- Мигание подсказки на старте ---
		self.show_start_message = True
		self.last_toggle_time = 0
		self.blink_interval = 0.7

	def draw_menu(self):
		surface = self.screen
		width, height = surface.get_size()

		bg = pygame.transform.scale(self.menu_background, (width, height))
		surface.blit(bg, (0, 0))

		# --- Название ---
		title_text = self.title_font.render("SNAKE", True, (255, 255, 255))
		title_rect = title_text.get_rect(center=(width // 2, height // 5))
		surface.blit(title_text, title_rect)

		# --- High Score ---
		high_score = self.game.max_score
		high_score_text = self.button_font.render(f"High Score: {high_score}", True, (255, 255, 255))
		high_score_rect = high_score_text.get_rect(center=(width // 2, height // 2 - 80))
		surface.blit(high_score_text, high_score_rect)

		# --- Кнопки ---
		button_size = (250, 80)
		start_pos = (width // 2 - button_size[0] // 2, height // 2)
		exit_pos = (width // 2 - button_size[0] // 2, height // 2 + button_size[1] + 30)

		self.game.start_button_rect = pygame.Rect(start_pos, button_size)
		self.game.exit_button_rect = pygame.Rect(exit_pos, button_size)

		# Кнопка старт
		start_img = pygame.transform.scale(self.button_bg, button_size)
		surface.blit(start_img, self.game.start_button_rect)
		start_text = self.button_font.render("Start Game", True, (255, 255, 255))
		surface.blit(start_text, start_text.get_rect(center=self.game.start_button_rect.center))

		# Кнопка выход
		exit_img = pygame.transform.scale(self.button_bg, button_size)
		surface.blit(exit_img, self.game.exit_button_rect)
		exit_text = self.button_font.render("Exit", True, (255, 255, 255))
		surface.blit(exit_text, exit_text.get_rect(center=self.game.exit_button_rect.center))

		# --- Громкость ---
		vol = self.game.music_volume
		volume_text = self.button_font.render(f"Volume: {vol}/10", True, (255, 255, 255))
		volume_text_rect = volume_text.get_rect(center=(width // 2, height - 200))
		surface.blit(volume_text, volume_text_rect)

		for i, rect in enumerate(self.volume_rects):
			img = self.vol_img_active if i < vol else self.vol_img_inactive
			surface.blit(img, rect.topleft)

	def draw_pause(self):
		surface = self.screen
		width, height = surface.get_size()

		overlay = pygame.Surface((width, height))
		overlay.set_alpha(40)
		overlay.fill((0, 0, 0))
		self.screen.blit(overlay, (0, 0))

		text = self.pause_font.render("PAUSE", True, (0, 150, 0))
		text_rect = text.get_rect(center=(width // 2, height // 2 - 100))
		self.screen.blit(text, text_rect)

		# --- Кнопки ---
		button_size = (250, 80)
		start_pos = (width // 2 - button_size[0] // 2, height // 2)
		exit_pos = (width // 2 - button_size[0] // 2, height // 2 + button_size[1] + 30)

		self.game.continue_button_rect = pygame.Rect(start_pos, button_size)
		self.game.menu_button_rect = pygame.Rect(exit_pos, button_size)

		# Кнопка продолжить
		continue_img = pygame.transform.scale(self.button_bg, button_size)
		surface.blit(continue_img, self.game.continue_button_rect)
		continue_text = self.button_font.render("Continue", True, (255, 255, 255))
		surface.blit(continue_text, continue_text.get_rect(center=self.game.continue_button_rect.center))
		# Кнопка меню
		menu_img = pygame.transform.scale(self.button_bg, button_size)
		surface.blit(menu_img, self.game.menu_button_rect)
		menu_text = self.button_font.render("Menu", True, (255, 255, 255))
		surface.blit(menu_text, menu_text.get_rect(center=self.game.menu_button_rect.center))

	def draw_game_over(self):
		surface = self.screen
		width, height = surface.get_size()

		overlay = pygame.Surface((width, height))
		overlay.set_alpha(150)
		overlay.fill((0, 0, 0))
		surface.blit(overlay, (0, 0))

		# Надпись "Игра окончена"
		title_text = self.title_font.render("Game Over", True, (255, 0, 0))
		title_rect = title_text.get_rect(center=(width // 2, height // 4))
		surface.blit(title_text, title_rect)

		# Кнопки "Начать заново" и "Выйти в меню"
		button_size = (250, 80)
		restart_pos = (width // 2 - button_size[0] // 2, height // 2)
		menu_pos = (width // 2 - button_size[0] // 2, height // 2 + button_size[1] + 30)

		self.restart_button_rect = pygame.Rect(restart_pos, button_size)
		self.back_to_menu_button_rect = pygame.Rect(menu_pos, button_size)

		# Кнопка "Начать заново"
		restart_img = pygame.transform.scale(self.button_bg, button_size)
		surface.blit(restart_img, self.restart_button_rect)
		restart_text = self.button_font.render("Again", True, (255, 255, 255))
		surface.blit(restart_text, restart_text.get_rect(center=self.restart_button_rect.center))

		# Кнопка "Выйти в меню"
		menu_img = pygame.transform.scale(self.button_bg, button_size)
		surface.blit(menu_img, self.back_to_menu_button_rect)
		menu_text = self.button_font.render("Menu", True, (255, 255, 255))
		surface.blit(menu_text, menu_text.get_rect(center=self.back_to_menu_button_rect.center))

	def draw_start_message(self):
		if self.game.waiting_flag:
			text = self.score_font.render("Press key to start", True, (0, 150, 0))
			rect = text.get_rect(center=self.screen.get_rect().center)
			self.screen.blit(text, rect)

