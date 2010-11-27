#!/usr/bin/env python
import pygame
import constants
from physical_object import PhysicalObject


TURRET_WIDTH = 24
TURRET_HEIGHT = 28

class Turret(PhysicalObject):
	"""This class represents a turret"""


	def __init__(self, position):

		PhysicalObject.__init__(self, position)

		self.physicsRect = pygame.rect.Rect(self.r_x, self.r_y, TURRET_WIDTH, TURRET_HEIGHT)
		
		self.image = pygame.image.load('images/defenses.png')
		self.rect = self.image.get_rect()
		
		self.actions = {"all": (0, 112, TURRET_WIDTH, TURRET_HEIGHT)}
		
		self.action = "all"
		self.area = pygame.rect.Rect(self.actions[self.action])
		#print 'turret (x,y) = ', (self.r_x, self.r_y)

		
