import sys
from pygame.math import Vector2
from game import Game
from UI import UI
from settings import *
import time

pygame.init()
pygame.mixer.init()
title_font = pygame.font.Font(font, 60)
score_font = pygame.font.Font(font, 40)
pygame.mixer.music.load("assets/sounds/bg_music.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)
pygame.display.set_caption("Medival Snake")

clock = pygame.time.Clock()

game = Game()
UI = UI(game)

SNAKE_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SNAKE_UPDATE, 200)

while True:
	for event in pygame.event.get():
		if event.type == SNAKE_UPDATE:
			game.update()
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.type == pygame.KEYDOWN:
				if game.state in ["WAITING", "RUNNING"]:
					new_direction = None
					if game.snake.reversed_controls:
						if event.key == pygame.K_UP:
							new_direction = Vector2(0, 1)
						elif event.key == pygame.K_DOWN:
							new_direction = Vector2(0, -1)
						elif event.key == pygame.K_LEFT:
							new_direction = Vector2(1, 0)
						elif event.key == pygame.K_RIGHT:
							new_direction = Vector2(-1, 0)
					else:
						if event.key == pygame.K_UP:
							new_direction = Vector2(0, -1)
						elif event.key == pygame.K_DOWN:
							new_direction = Vector2(0, 1)
						elif event.key == pygame.K_LEFT:
							new_direction = Vector2(-1, 0)
						elif event.key == pygame.K_RIGHT:
							new_direction = Vector2(1, 0)

					if new_direction:
						if new_direction and not game.snake.direction_changed:
							# Проверка на то, что новое направление не противоположно текущему
							if new_direction + game.snake.direction != Vector2(0, 0):
								game.snake.direction = new_direction
								game.snake.direction_changed = True
								if game.state == "WAITING" and game.is_starting:
									game.state = "RUNNING"
									game.is_starting = False

						else:
							# Нажата пстрелка противоположная текущему движению - ничего не происходит
							pass

		if game.state == "MENU":
			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				for idx, rect in enumerate(UI.volume_rects, start=1):
					if rect.collidepoint(event.pos):
						UI.game.music_volume = idx
						print(idx)
						pygame.mixer.music.set_volume(UI.game.music_volume / 10)
						print(UI.game.music_volume)
						break
				if UI.game.start_button_rect.collidepoint(event.pos):
					game.reset()
				elif UI.game.exit_button_rect.collidepoint(event.pos):
					pygame.quit()
					sys.exit()

		# Пауза
		if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			if game.state == "RUNNING":
				game.state = "PAUSED"
			elif game.state == "PAUSED":
				# Если стартовая фаза, возвращаем в WAITING, но не запускаем игру
				if game.is_starting:
					game.state = "WAITING"
				else:
					game.state = "RUNNING"
			elif game.state == "WAITING":
				game.state = "PAUSED"

		if game.state == "PAUSED":
			UI.draw_pause()
			# Клики по кнопкам паузы
			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				if UI.game.continue_button_rect.collidepoint(event.pos):
					game.state = "RUNNING"
				elif UI.game.menu_button_rect.collidepoint(event.pos):
					game.state = "MENU"
		#смерть
		if game.state == "DEAD":
			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				if game.ui.restart_button_rect.collidepoint(event.pos):
					game.reset()
				elif game.ui.back_to_menu_button_rect.collidepoint(event.pos):
					game.state = "MENU"

	#Drawing
	bg_raw = pygame.image.load("assets/images/game_bg.png").convert()
	surface = pygame.display.get_surface()
	surface.blit(bg_raw, (0, 0))
	pygame.draw.rect(screen, DARK_GREEN,
		(OFFSET-5, OFFSET-5, cell_size*number_of_cells+10, cell_size*number_of_cells+10), 5)

	# Мигание подсказки
	if game.state == "WAITING":
		current_time = time.time()
		if current_time - game.last_toggle_time > game.blink_interval:
			game.waiting_flag = not game.waiting_flag
			game.last_toggle_time = current_time

	game.draw()

	pygame.display.update()
	clock.tick(60)