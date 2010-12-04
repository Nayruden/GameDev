#!/usr/bin/env python
import pygame
import constants
import physical_object
from network import Type
from physical_object import PhysicalObject



BULLET_WIDTH = 12
BULLET_HEIGHT = 14

# behavioral constants; these numbers were chosen because they feel about right
DEFAULT_SPEED = 7 + constants.SCROLL_RATE  # a little faster than the ship's max. speed
LIFE_SPAN = 45  # in frames at the moment

class Bullet(PhysicalObject):
	"""This class represents a generic bullet"""
	timeToLive = 0
	typ = Type.TBULLET # Start Bullets generically as a turret bullet	 
	
	def __init__(self, position, bulletkind):
		
		PhysicalObject.__init__(self, position)

		self.collisionType = physical_object.COLLISION_TYPE_BULLET
		self.physicsRect = pygame.rect.Rect(self.r_x, self.r_y, BULLET_WIDTH, BULLET_HEIGHT)

		self.image = pygame.image.load('images/bullets.png')
		self.rect = self.image.get_rect()

		self.kinds = {"shp": (0, 0, self.physicsRect.width, self.physicsRect.height),
			      "tur": (12, 0, self.physicsRect.width, self.physicsRect.height)}

		self.kind = bulletkind
		self.area = pygame.rect.Rect(self.kinds[self.kind])

		self.timeToLive = LIFE_SPAN

		#print("Bullet's physics rectangle: ", self.physicsRect);


	def step(self, scrollPosition):
		PhysicalObject.step(self, scrollPosition)
		self.timeToLive -= 1
		if(self.timeToLive <= 0):  self.destroyed = True;


	def resolveCollisionWith(self, otherObject):
		if otherObject.collisionType != physical_object.COLLISION_TYPE_BULLET and otherObject.controllingPlayer != self.controllingPlayer:
			self.destroyed = True

