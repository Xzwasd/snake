from food import Food
from snake import Snake
from settings import *
from UI import UI
import time, json, os



class Game:
	def __init__(self):
		self.snake = Snake()
		self.food = Food(self.snake.body)
		self.state = "MENU"
		self.score = 0
		self.max_score = self.load_max_score()
		self.music_volume = 5
		pygame.mixer.music.set_volume(self.music_volume / 10)
		self.ui = UI(self)
		# Мигание подсказки
		self.waiting_flag = True
		self.is_starting = True
		self.last_toggle_time = time.time()
		self.blink_interval = 0.7
		self.game_time = 0  # внутриигровое время в секундах
		self.last_time_update = None

	def draw(self):
		if self.state == 'MENU':
			self.ui.draw_menu()
		else:
			self.food.draw()
			self.snake.draw()
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
				self.game_time += current_time - self.last_time_update  # увеличиваем внутриигровое время
			self.last_time_update = current_time

			# Проверка таймера еды
			if self.game_time - self.food.spawn_game_time > 7:
				self.food.respawn(self.snake.body, self.game_time)

			self.snake.update()
			self.check_collision_with_food()
			self.check_collision_with_edges()
			self.check_collision_with_tail()
		else:
			self.last_time_update = None  # Останавливаем счёт при паузе

	def check_collision_with_food(self):
		if self.snake.body[0] == self.food.position:
			self.food.respawn(self.snake.body, self.game_time)
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
		self.state = "DEAD"
		#self.snake.wall_hit_sound.play()
		self.food.respawn(self.snake.body, self.game_time)

	def reset(self): #новая игра
		self.snake = Snake()
		self.food = Food(self.snake.body)
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