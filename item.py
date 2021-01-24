import pygame
import os
import random

class Item:
	def __init__(self, x, y):
		self.location = (x, y)
		self.loadAssets()

	def loadAssets(self):
		num = {
			0 : 'pokeball.png',
			1 : 'starman.png',
			2 : 'heart.png'
		}
		self.img = pygame.image.load(os.path.join('assets', 'powerup', num[random.randrange(0, 3)]))