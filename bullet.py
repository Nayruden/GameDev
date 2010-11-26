#!/usr/bin/env python
import pygame
import constants
from physical_object import PhysicalObject

# behavioral constants; these numbers were chosen because they feel about right
DEFAULT_SPEED = 7  # a little faster than the ship's max. speed
LIFE_SPAN = 45  # in frames at the moment

class Bullet(PhysicalObject):
	"""This class represents a generic bullet"""
	timeToLive = 0


	def __init__(self, position):

		PhysicalObject.__init__(self, position)

		self.physicsRect = pygame.rect.Rect(self.r_x, self.r_y, 20, 34)
		
		self.image = pygame.image.load('images/projectiles.png')
		self.rect = self.image.get_rect()
		
		self.actions = {"all": (167, 113, self.physicsRect.width, self.physicsRect.height)}
		
		self.action = "all"
		self.area = pygame.rect.Rect(self.actions[self.action])

		self.timeToLive = LIFE_SPAN

		#print("Bullet's physics rectangle: ", self.physicsRect);


	def step(self, scrollPosition):
		PhysicalObject.step(self, scrollPosition)
		self.timeToLive -= 1
		if(self.timeToLive <= 0):  self.destroyed = True;
		
