#!/usr/bin/python 
import pygame
import sys
import time
import random
import multiprocessing
from cv2_daemon import CameraDaemon
from player import *
from item import *
from math import floor, ceil

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
)

class EyeSnake:
	def __init__(self, args=[0]):
		self.args = args
		pygame.init()
		self.screen = pygame.display.set_mode([800, 800])
		self.run = True
		self.player = Player()
		self.dydx_multi = 1
		self.clock = pygame.time.Clock()
		self.grid = [x for x in range(0, self.screen.get_width(), 80)]
		self.prev_pos_x = []
		self.prev_pos_y = []
		self.placeItem()
		self.game_loop()

	def setArg(self, val):
		self.args[0] = val

	def getArg(self):
		return self.args[0]
		
	def on_render(self):
		self.screen.fill((255, 255, 255))
		self.screen.blit(self.player.head, (self.grid[int(self.player.x[0])], self.grid[int(self.player.y[0])]))
		for x in range(1, self.player.nTail):
			self.screen.blit(self.player.body, (self.grid[int(self.prev_pos_x[x])], self.grid[int(self.prev_pos_y[x])]))
		self.screen.blit(self.currItem.img, (self.grid[self.currItem.location[0]], self.grid[self.currItem.location[1]]))
		pygame.display.flip()
	
	def on_event(self, event):
		if event.type == pygame.QUIT:
			self.run = False

	def checkBoundsX(self):
		return self.player.x[0] >= 0 and self.player.x[0] < self.screen.get_width()

	def checkBoundsY(self):
		return self.player.y[0] >= 0 and self.player.y[0] < self.screen.get_height()

	def checkSnakeTouchingSelf(self):
		for i in range(1, len(self.player.x)):
			if self.player.x[0] == self.prev_pos_x[i] and self.prev_pos_y[0] == self.player.y[i]:
				return True
		return False

	def setDirection(self, newDirection):
		if newDirection == self.player.direction:
			return
		angle = (self.player.direction - newDirection) * 90
		self.player.direction = newDirection
		self.player.head = pygame.transform.rotate(self.player.head, angle)

	def placeItem(self):
		self.currItem = Item(random.randrange(0, (self.screen.get_width() / 80) - 1), random.randrange(0, (self.screen.get_width() / 80) - 1))

	def checkSnakeTouchingItem(self):
		return int(self.player.x[0]) == self.currItem.location[0] and int(self.player.y[0]) == self.currItem.location[1]

	def game_loop(self):
		while self.run:		
			pygame.event.poll()
			keys = pygame.key.get_pressed()

			if self.getArg():
				self.dydx_multi = 3

			self.prev_pos_x.insert(0, self.player.x[0])
			self.prev_pos_y.insert(0, self.player.y[0])

			if keys[K_RIGHT] and self.checkBoundsX():
				self.player.dx = 1 * self.dydx_multi
				self.player.dy = 0 * self.dydx_multi
				self.setDirection(0)

			if keys[K_UP] and self.checkBoundsY():
				self.player.dx = 0 * self.dydx_multi
				self.player.dy = -1 * self.dydx_multi
				self.setDirection(3)

			if keys[K_LEFT] and self.checkBoundsX():
				self.player.dx = -1 * self.dydx_multi
				self.player.dy = 0 * self.dydx_multi
				self.setDirection(2)

			if keys[K_DOWN] and self.checkBoundsY():
				self.player.dx = 0 * self.dydx_multi
				self.player.dy = 1 * self.dydx_multi
				self.setDirection(1)

			if keys[K_ESCAPE]:
				sys.exit(1)

			if self.checkSnakeTouchingItem():
				self.player.nTail += 1
				self.prev_pos_x.append(self.grid[int(self.player.x[0])])
				self.prev_pos_y.append(self.grid[int(self.player.y[0])])
				self.placeItem()
				
			self.player.update_pos(1 / float(self.clock.tick(60)))
			if not self.checkBoundsX() or not self.checkBoundsY() or self.checkSnakeTouchingSelf():
				print("Game over")
				break
			self.on_render()		

if __name__ == "__main__":	
	EyeSnake()