import json
import random
from pygame.math import Vector2
from settings import *

class Walls:
	def __init__(self):
		self.blocks = []
		self.image = pygame.image.load("assets/images/wall.png").convert_alpha()
		self.image = pygame.transform.scale(self.image, (cell_size, cell_size))
		self.load_random_layout()

	def load_random_layout(self):
		with open("data/walls.json", "r") as file:
			layouts = json.load(file)["layouts"]
			layout = random.choice(layouts)
			self.blocks = [Vector2(pos[0], pos[1]) for pos in layout]

	def draw(self, surface):
		for block in self.blocks:
			pos = (OFFSET + block.x * cell_size, OFFSET + block.y * cell_size)
			surface.blit(self.image, pos)

	def collides_with(self, position):
		return position in self.blocks
