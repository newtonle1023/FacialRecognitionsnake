import pygame
import os

class Player:
	def __init__(self):
		self.x = [4]
		self.y = [4]
		self.dx = 1
		self.dy = 0
		self.direction = 0
		self.nTail = 1
		self.loadAssets()

	def update_pos(self, dt): 
		self.x[0] += self.dx * dt
		self.y[0] += self.dy * dt

	def loadAssets(self):
		self.head = pygame.image.load(os.path.join('assets', 'snake', 'head.png'))
		self.body = pygame.image.load(os.path.join('assets', 'snake', 'body.png'))