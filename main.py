import pygame, sys, random
from pygame.math import Vector2
from game import Game
from settings import *

pygame.init()
title_font = pygame.font.Font(None, 60)
score_font = pygame.font.Font(None, 40)

pygame.display.set_caption("Retro Snake")

clock = pygame.time.Clock()

game = Game()

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
				if game.state == "STOPPED":
					game.state = "WAITING"
					game.show_start_message = False

				if game.state in ["WAITING", "RUNNING"]:
					new_direction = None
					if event.key == pygame.K_UP:
						new_direction = Vector2(0, -1)
					elif event.key == pygame.K_DOWN:
						new_direction = Vector2(0, 1)
					elif event.key == pygame.K_LEFT:
						new_direction = Vector2(-1, 0)
					elif event.key == pygame.K_RIGHT:
						new_direction = Vector2(1, 0)

					if new_direction:
						# Проверка на то, что новое направление не противоположно текущему
						if new_direction + game.snake.direction != Vector2(0, 0):
							game.snake.direction = new_direction
							if game.state == "WAITING":
								game.state = "RUNNING"
						else:
							# Нажата пстрелка противоположная текущему движению - ничего не происходит
							pass

	#Drawing
	screen.fill(GREEN)
	pygame.draw.rect(screen, DARK_GREEN,
		(OFFSET-5, OFFSET-5, cell_size*number_of_cells+10, cell_size*number_of_cells+10), 5)
	game.draw()
	title_surface = title_font.render("Retro Snake", True, DARK_GREEN)
	score_surface = score_font.render(str(game.score), True, DARK_GREEN)
	screen.blit(title_surface, (OFFSET-5, 20))
	screen.blit(score_surface, (OFFSET-5, OFFSET + cell_size*number_of_cells +10))

	if game.state == "WAITING" and game.show_start_message:
		start_surface = score_font.render("Press key to start", True, DARK_GREEN, GREEN)
		text_rect = start_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
		screen.blit(start_surface, text_rect)

	pygame.display.update()
	clock.tick(60)