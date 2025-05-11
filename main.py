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
			if game.state == "STOPPED":
				game.state = "RUNNING"
			if event.key == pygame.K_UP and game.snake.direction != Vector2(0, 1):
				game.snake.direction = Vector2(0, -1)
			if event.key == pygame.K_DOWN and game.snake.direction != Vector2(0, -1):
				game.snake.direction = Vector2(0, 1)
			if event.key == pygame.K_LEFT and game.snake.direction != Vector2(1, 0):
				game.snake.direction = Vector2(-1, 0)
			if event.key == pygame.K_RIGHT and game.snake.direction != Vector2(-1, 0):
				game.snake.direction = Vector2(1, 0)

	#Drawing
	screen.fill(GREEN)
	pygame.draw.rect(screen, DARK_GREEN,
		(OFFSET-5, OFFSET-5, cell_size*number_of_cells+10, cell_size*number_of_cells+10), 5)
	game.draw()
	title_surface = title_font.render("Retro Snake", True, DARK_GREEN)
	score_surface = score_font.render(str(game.score), True, DARK_GREEN)
	screen.blit(title_surface, (OFFSET-5, 20))
	screen.blit(score_surface, (OFFSET-5, OFFSET + cell_size*number_of_cells +10))

	pygame.display.update()
	clock.tick(60)