#!/usr/bin/env python
import pygame
import constants


class PhysicalObject(pygame.sprite.Sprite):
	"""This class represents a generic physical object"""

	childObjects = []  # temporary storage for physical objects created by this object (such as bullets)

	area = pygame.rect.Rect(0, 0, 0, 0)
	rect = pygame.rect.Rect(0, 0, 0, 0)
	physicsRect = pygame.rect.Rect(0, 0, 0, 0)
	destroyed = False
	r_x = 0.0  # location x; I didn't want to use something as generic as "x" and "y", so I pulled from physics/engineering convention
	r_y = 0.0  # location y
	v_x = 0.0  # velocity x
	v_y = 0.0  # velocity y
	LEFT = False
	RIGHT = False
	UP = False
	DOWN = False


	def __init__(self, position):

		pygame.sprite.Sprite.__init__(self)
		self.setX(position[0])
		self.setY(position[1])


	def step(self, scrollPosition):

		#update position
		self.setX(self.getX() + self.v_x)
		self.setY(self.getY() + self.v_y - constants.SCROLL_RATE)


	def getX(self):
		return self.r_x

	def setX(self, newX):
		self.r_x = newX
		self.rect.x = self.r_x
		self.physicsRect.x = self.r_x

	def getY(self):
		return self.r_y

	def setY(self, newY):
		self.r_y = newY
		self.rect.y = self.r_y
		self.physicsRect.y = self.r_y

	def setPosition(self, newX, newY):
		self.setX(self, newX)
		self.setY(self, newY)
