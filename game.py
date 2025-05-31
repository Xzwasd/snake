from food import Food, BigFood, PoisonFood, ReversedFood
from snake import Snake
from settings import *
from wall import Walls
from UI import UI
import time, json, os
import random


class Game:
	def __init__(self):
		self.walls = Walls()
		self.snake = Snake(self.walls.blocks)
		self.food = Food(self.snake.body, self.walls.blocks)
		self.state = "MENU"
		self.score = 0
		self.max_score = self.load_max_score()

		self.ui = UI(self)

		# Мигание подсказки
		self.waiting_flag = True
		self.is_starting = True
		self.last_toggle_time = time.time()
		self.blink_interval = 0.7

		self.game_time = 0
		self.last_time_update = None

		self.special_food = None
		self.special_food_cooldown = 15
		self.special_food_lifetime = 10
		self.last_special_food_spawn_time = 0

		self.music_volume = 5
		pygame.mixer.music.set_volume(self.music_volume / 10)
		self.death_sound = pygame.mixer.Sound("assets/sounds/death_sound.mp3")
		self.eating_sound = pygame.mixer.Sound("assets/sounds/eating_sound.mp3")
		self.drinking_sound = pygame.mixer.Sound("assets/sounds/drinking_sound.mp3")
		self.drinking_sound.set_volume(0.4)

	def draw(self):
		if self.state == 'MENU':
			self.ui.draw_menu()
		else:
			self.food.draw()
			self.snake.draw()
			if self.special_food:
				self.special_food.draw()
			self.walls.draw(self.ui.screen)
			if self.state == "WAITING":
				self.ui.draw_start_message()
				self.ui.draw_score()
			elif self.state == "PAUSED":
				self.ui.draw_pause()
			elif self.state == "DEAD":
				self.ui.draw_game_over()
			elif self.state == "RUNNING":
				self.ui.draw_score()


	def update(self):
		if self.state == "RUNNING":
			current_time = time.time()
			if self.last_time_update is not None:
				self.game_time += current_time - self.last_time_update
			self.last_time_update = current_time

			# Проверка таймера еды
			if self.game_time - self.food.spawn_game_time > 7:
				self.food.respawn(self.snake.body, self.game_time)

			self.snake.update()
			self.check_collision_with_food()
			self.check_collision_with_edges()
			self.check_collision_with_tail()
			self.check_collision_with_walls()

			# Удаление BigFood / PoisonFood, если прошло 10 сек
			if self.special_food and self.game_time - self.special_food.spawn_game_time >= self.special_food_lifetime:
				self.special_food = None

			if self.special_food is None and self.game_time - self.last_special_food_spawn_time >= self.special_food_cooldown:
				self.special_food = random.choice([
					BigFood(self.snake.body),
					PoisonFood(self.snake.body),
					ReversedFood(self.snake.body)
				])
				self.special_food.spawn_game_time = self.game_time
				self.last_special_food_spawn_time = self.game_time

			self.check_collision_with_special_food()

		else:
			self.last_time_update = None  # Останавливаем счёт при паузе

	def check_collision_with_walls(self):
		if self.walls.collides_with(self.snake.body[0]):
			self.game_over()

	def check_collision_with_food(self):
		if self.snake.body[0] == self.food.position:
			self.food.respawn(self.snake.body, self.game_time)
			self.snake.add_segment = True
			self.score += 1
			self.eating_sound.play()

	def check_collision_with_special_food(self):
		if self.special_food and self.snake.body[0] == self.special_food.position:
			if isinstance(self.special_food, BigFood):
				self.snake.add_segment = 3
				self.score += 3
			elif isinstance(self.special_food, PoisonFood):
				for _ in range(3):
					if len(self.snake.body) > 3:
						self.snake.body.pop()
					else:
						self.game_over()
						return
			elif isinstance(self.special_food, ReversedFood):
				self.snake.reversed_controls = True
				self.snake.reverse_end_time = time.time() + 7

			self.drinking_sound.play()
			self.special_food = None

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
		self.food.position = self.food.generate_random_pos(self.snake.body)
		self.state = "DEAD"
		self.food.respawn(self.snake.body, self.game_time)
		self.death_sound.play()

	def reset(self): #новая игра
		self.walls = Walls()
		self.snake = Snake(self.walls.blocks)
		self.food = Food(self.snake.body, self.walls.blocks)
		self.special_food = None
		self.score = 0
		self.state = "WAITING"
		self.waiting_flag = True
		self.is_starting = True
		self.game_time = 0
		self.last_time_update = None

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