#!/usr/bin/env python
import pygame
import constants
import play_sound
from pygame import mixer
from pygame.mixer import Sound

COLLISION_TYPE_UNDEF = 0
COLLISION_TYPE_GROUND = 1
COLLISION_TYPE_BULLET = 2
COLLISION_TYPE_SHIP = 3

OWNER_NONE = 0
OWNER_ATTACKER = OWNER_NONE + 1
OWNER_DEFENDER = OWNER_ATTACKER + 1

NO_OBJECT_ID = -1
INITIAL_OBJECT_ID = NO_OBJECT_ID + 1

class PhysicalObject(pygame.sprite.Sprite):
	"""This class represents a generic physical object"""

	# class variable
	nextObjectID = INITIAL_OBJECT_ID

	# instance variables
	childObjects = []  # temporary storage for physical objects created by this object (such as bullets)
	networkID = None
	controllingPlayer = OWNER_NONE

	# more instance variables
	objectID = NO_OBJECT_ID
	area = pygame.rect.Rect(0, 0, 0, 0)
	rect = pygame.rect.Rect(0, 0, 0, 0)
	physicsRect = pygame.rect.Rect(0, 0, 0, 0)
	collisionType = COLLISION_TYPE_UNDEF
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
		self.objectID = PhysicalObject.nextObjectID
		PhysicalObject.nextObjectID += 1
		#print "Constructing object with object ID ", self.objectID


	def step(self, scrollPosition):

		#update position
		self.setX(self.getX() + self.v_x)
		self.setY(self.getY() + self.v_y)


	def resolveCollisionWith(self, otherObject):
		# apply collision effects to this object, not the other object
		if otherObject.collisionType == COLLISION_TYPE_BULLET and otherObject.controllingPlayer != self.controllingPlayer:
			self.destroyed = True
			explode = pygame.mixer.Sound(constants.EXPLOSION_SFX)
			explode.set_volume(0.4)
			play_sound.PlaySounds(explode)


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

	def getVX(self):
		return self.v_x

	def getVY(self):
		return self.v_y

	def setPosition(self, newX, newY):
		self.setX(self, newX)
		self.setY(self, newY)
