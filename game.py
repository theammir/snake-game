import numpy
import pygame
import random
from pygame import gfxdraw
pygame.init()

config_instance = open('settings.txt', 'r', encoding = 'utf-8')

class Settings:
	def __init__(self, settings: dict):
		def str_to_rgb(sequence):
			r, g, b = sequence.split(' ')
			r, g, b = int(r), int(g), int(b)
			if (any([r not in range(0, 255), g not in range(0, 255), b not in range(0, 255)])):
				raise ValueError(f'You set wrong colour values, check your settings! ({r, g, b})') # wrong rgb color values
			return (r, g, b)
		setting_names = {
			'size of cell': ('cellsize', int), 	
			'size of grid':   ('gridsize', int),
			'snake colour': 'snake_color',
			'apple colour': 'apple_color',
			'default length': ('snake_len', int)
		}
		for key, value in settings.items():
			if (setting_names.get(key)):
				if (isinstance(setting_names[key], tuple)):
					setattr(self, setting_names[key][0], setting_names[key][1](value))
				else:
					setattr(self, setting_names[key], value)

		if (getattr(self, 'snake_color', None)):
			self.snake_color = str_to_rgb(self.snake_color)
		else:
			self.snake_color = (10, 240, 100) # default color

		if (getattr(self, 'apple_color', None)):
			self.apple_color = str_to_rgb(self.apple_color)
		else:
			self.apple_color = (240, 10, 10) # default color

def file_handler(instance):
	text = instance.read().split('\n')
	settings = {}
	for line in text:
		line = line.split(' - ')
		line[0] = line[0].strip(); line[1] = line[1].strip()
		settings[line[0]] = line[1]
	return Settings(settings)
settings = file_handler(config_instance)


class Game:
	def __init__(self, settings):
		self.settings = settings
		self.clock = pygame.time.Clock()
		self.loop = False
		self.display = pygame.display.set_mode((self.settings.gridsize * self.settings.cellsize, self.settings.gridsize * self.settings.cellsize))
		self.snake: list = []
		self.apple: list = []
		self.direction: str = 'right'

		middle = self.settings.gridsize // 2
		xcoords = [middle + i for i in range(self.settings.snake_len)]
		ycoords = [middle for _ in range(self.settings.snake_len)] # default snake position
		for x, y in zip(xcoords, ycoords):
			self.snake.append((x, y))

		pygame.display.set_caption('Snake Game')

	def start(self):
		self.loop = True

		self.spawn_apple()

		while (self.loop):
			for e in pygame.event.get():
				if (e.type == pygame.QUIT):
					self.loop = False
				if (e.type == pygame.KEYDOWN):
					if (e.key in [pygame.K_w, pygame.K_UP] and self.direction != 'down'):
						self.direction = 'up'
					elif (e.key in [pygame.K_s, pygame.K_DOWN] and self.direction != 'up'):
						self.direction = 'down'
					elif (e.key in [pygame.K_d, pygame.K_RIGHT] and self.direction != 'left'):
						self.direction = 'right'
					elif (e.key in [pygame.K_a, pygame.K_LEFT] and self.direction != 'right'):
						self.direction = 'left'

			self.clock.tick(15)
			self.display.fill((0, 0, 0))
			self.move_snake()
			self.draw()

			pygame.display.update()

	def move_snake(self):
		self.snake.pop(0)
		if (self.direction == 'left'):
			self.snake.append((self.snake[-1][0] - 1, self.snake[-1][1]))
		elif (self.direction == 'right'):
			self.snake.append((self.snake[-1][0] + 1, self.snake[-1][1]))
		elif (self.direction == 'up'):
			self.snake.append((self.snake[-1][0], self.snake[-1][1] - 1))
		elif (self.direction == 'down'):
			self.snake.append((self.snake[-1][0], self.snake[-1][1] + 1))

		if (self.snake[-1] == tuple(self.apple)):
			self.add_snakes_length(self.direction)
			self.spawn_apple()

		if (self.snake[-1] in self.snake[:-1]):
			self.loop = False
			print(f'You lose. Score: {len(self.snake) - self.settings.snake_len}')

		if (self.snake[-1][0] < 0 or self.snake[-1][1] < 0 or self.snake[-1][0] > self.settings.cellsize or self.snake[-1][1] > self.settings.cellsize):
			self.loop = False
			print(f'You lose. Score: {len(self.snake) - self.settings.snake_len}')


	def spawn_apple(self):
		in_snake = True
		while (in_snake):
			apple_x = random.randint(0, self.settings.gridsize - 1)
			apple_y = random.randint(0, self.settings.gridsize - 1)
			if ((apple_x, apple_y) not in self.snake and (apple_x, apple_y) != self.apple):
				in_snake = False
				self.apple = [apple_x, apple_y]

	def add_snakes_length(self, direction):
		if (direction == 'up'):
			self.snake.insert(0, (self.snake[0][0], self.snake[0][1] + 1))
		elif (direction == 'down'):
			self.snake.insert(0, (self.snake[0][0], self.snake[0][1] - 1))
		elif (direction == 'left'):
			self.snake.insert(0, (self.snake[0][0], self.snake[0][1] + 1))
		elif (direction == 'right'):
			self.snake.insert(0, (self.snake[0][0], self.snake[0][1] - 1))

	def draw(self):
		cellsize = self.settings.cellsize
		gfxdraw.box(self.display, (self.apple[0] * cellsize, self.apple[1] * cellsize, cellsize, cellsize), self.settings.apple_color)
		for x, y in self.snake:
			gfxdraw.box(self.display, (x * cellsize, y * cellsize, cellsize, cellsize), self.settings.snake_color)



game = Game(settings)

game.start()