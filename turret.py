#!/usr/bin/env python
import pygame
import constants
from network import Type
import physical_object
from physical_object import PhysicalObject
import bullet

import math

from pygame.rect import Rect
import play_sound
from pygame import mixer
from pygame.mixer import Sound
TURRET_WIDTH = 24
TURRET_HEIGHT = 28

GUN_COOLDOWN_TIME = 100

class Turret(PhysicalObject):
	"""This class represents a turret"""

	typ = Type.TURRET
	timeUntilWeaponCanFireAgain = 0
	

	def __init__(self, position, level):

		PhysicalObject.__init__(self, position)

		self.level = level
		self.controllingPlayer = physical_object.OWNER_DEFENDER

		self.physicsRect = pygame.rect.Rect(self.r_x, self.r_y, TURRET_WIDTH, TURRET_HEIGHT)

		self.image = pygame.image.load('images/defenses.png')
		self.rect = self.image.get_rect()

		self.actions = {"all": (0, 112, TURRET_WIDTH, TURRET_HEIGHT)}

		self.boundsRect = Rect(level.rect.x,level.rect.y,level.rect.width,constants.SCREEN_HEIGHT)

		self.action = "all"
		self.area = pygame.rect.Rect(self.actions[self.action])
		#print 'turret (x,y) = ', (self.r_x, self.r_y)
		#print 'turret owner = ', self.controllingPlayer


	def step(self, scrollPosition):

		# translate movement boundary
		self.boundsRect.y = scrollPosition
		
		# update position
		PhysicalObject.step(self, scrollPosition)
		if self.timeUntilWeaponCanFireAgain > 0:
			self.timeUntilWeaponCanFireAgain -= 1
				
		if self.physicsRect.colliderect(self.boundsRect):
			for o in self.level.physicalObjects:
				if(o.controllingPlayer == physical_object.OWNER_ATTACKER and
				o.targetType == physical_object.TARGET_TYPE_SHIP and
				self.timeUntilWeaponCanFireAgain <= 0):
					# it's the ship! get it!
					soundEfx = pygame.mixer.Sound(constants.TURRET_BULLET_SFX)
					soundEfx.set_volume(0.5)
					play_sound.PlaySounds(soundEfx)
					theBullet = bullet.Bullet((self.rect.x + TURRET_WIDTH/2 - bullet.BULLET_WIDTH/2, self.rect.y + (bullet.BULLET_HEIGHT + 6)), "tur")
					theBullet.controllingPlayer = self.controllingPlayer
					# old velocity code
					deltaX = o.r_x - self.r_x
					deltaY = o.r_y - self.r_y
					distance = math.hypot(deltaX, deltaY)
					theBullet.v_x = bullet.DEFAULT_SPEED*(deltaX/distance)  # v_x = speed*cos
					theBullet.v_y = bullet.DEFAULT_SPEED*(deltaY/distance)  # v_y = speed*sin
					# new velocity code; apparently tries to divide by zero and take the square root of a negative number
					#timeToImpact = ((o.r_x*o.v_x + o.r_y*o.v_y + math.sqrt(-pow(o.r_y,2)*(-1 + pow(o.v_x, 2)) + o.r_x*(o.r_x + 2*o.r_y*o.v_x*o.v_y - o.r_x*pow(o.v_y, 2))))/(-1 + pow(o.v_x, 2) + pow(o.v_y, 2)))
					#theBullet.v_x = (o.r_x + timeToImpact*o.v_x)/timeToImpact
					#theBullet.v_y = (o.r_y + timeToImpact*o.v_y)/timeToImpact
					self.childObjects.append(theBullet)
					self.timeUntilWeaponCanFireAgain = GUN_COOLDOWN_TIME
	
	

