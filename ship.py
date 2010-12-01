#!/usr/bin/env python
import pygame
import constants
from network import Type
from physical_object import PhysicalObject
import bullet

from pygame.rect import Rect
#imports for sound
import play_sound
from pygame import mixer
from pygame.mixer import Sound
#for AWESOME input!!! (fixing pygame's b0rked event handling)

SHIP_WIDTH = 46
SHIP_HEIGHT = 50

GUN_COOLDOWN_TIME = 10

class Ship(PhysicalObject):
	"""This class represents the ship"""

	timeUntilWeaponCanFireAgain = 0
	typ = Type.SHIP
	

	def __init__(self, position, level):

		PhysicalObject.__init__(self, position)
		self.level = level

		self.image = pygame.image.load('images/ship.png')
		self.rect = self.image.get_rect()

		self.actions = {	"center":	(SHIP_WIDTH*2, 0, SHIP_WIDTH,SHIP_HEIGHT),
			"left":	 (SHIP_WIDTH*0, 0, SHIP_WIDTH,SHIP_HEIGHT),
			"left-center":	(SHIP_WIDTH*1, 0, SHIP_WIDTH,SHIP_HEIGHT),
			"right-center":	(SHIP_WIDTH*3, 0, SHIP_WIDTH,SHIP_HEIGHT),
			"right":	(SHIP_WIDTH*4, 0, SHIP_WIDTH,SHIP_HEIGHT)
			}

		self.action = "center"
		self.area = pygame.rect.Rect(self.actions[self.action])

		self.boundsRect = Rect(level.rect.x,level.rect.y,level.rect.width,constants.SCREEN_HEIGHT)

		self.physicsRect = pygame.rect.Rect(self.r_x, self.r_y, SHIP_WIDTH, SHIP_HEIGHT)


	def step(self, scrollPosition):

			#tight physics
			v_step = 0.5
			v_target = 6.0  # max. speed relative to screen

			# translate movement boundary
			self.boundsRect.y = scrollPosition

			# determine speed
			def towards(current,expected):
				if abs(expected-current) < v_step: return expected
				if current > expected:
					return current - v_step
				return current + v_step

			# continue to determine speed
			if self.DOWN and not self.UP:
				self.v_y = towards(self.v_y,v_target-constants.SCROLL_RATE)
			elif self.UP and not self.DOWN:
				self.v_y = towards(self.v_y,-v_target-constants.SCROLL_RATE)
			elif not self.UP and not self.DOWN:
				self.v_y = towards(self.v_y,-constants.SCROLL_RATE)
			if self.LEFT and not self.RIGHT:
				self.v_x = towards(self.v_x,-v_target-constants.SCROLL_RATE)
			elif self.RIGHT and not self.LEFT:
				self.v_x = towards(self.v_x,v_target-constants.SCROLL_RATE)
			elif not self.LEFT and not self.RIGHT:
				self.v_x = towards(self.v_x,0)

			# update position
			PhysicalObject.step(self, scrollPosition)

			#hard bounds fix
			if self.physicsRect.x + self.physicsRect.width > self.boundsRect.x + self.boundsRect.width:
				self.setX(self.boundsRect.x + self.boundsRect.width - self.physicsRect.width)
			if self.r_x < self.boundsRect.x:
				self.setX(self.boundsRect.x)
			if self.r_y + self.physicsRect.height > self.boundsRect.y + self.boundsRect.height:
				self.setY(self.boundsRect.y + self.boundsRect.height - self.physicsRect.height)
			if self.r_y < self.boundsRect.y:
				self.setY(self.boundsRect.y)

			#update image
			if 0 < self.v_x < (v_target / 2.0):
				self.action = "right-center"
			elif (v_target / 2.0) <= self.v_x <= v_target:
				self.action = "right"
			elif self.v_x==0:
				self.action = "center"
			elif -(v_target / 2.0) < self.v_x < 0:
				self.action = "left-center"
			elif -(v_target) < self.v_x < -(v_target/2.0):
				self.action = "left"

			self.area = pygame.rect.Rect(self.actions[self.action])

			# update weapon
			if self.timeUntilWeaponCanFireAgain > 0:
				self.timeUntilWeaponCanFireAgain -= 1

			#print 'ship (x,y) = ', (self.r_x, self.r_y)


	def handle_event(self,event):
		handled_event = True
		#pygame's events are not very intelligent, so first of all let's fix them
		if event.type != pygame.KEYDOWN and event.type != pygame.KEYUP: return False
		if event.dict["key"]==274: #down
			self.DOWN = event.type==pygame.KEYDOWN and True or False
			#self.UP = False
		elif event.dict["key"]==273: #up
			self.UP = event.type==pygame.KEYDOWN and True or False
			#self.DOWN = False
		elif event.dict["key"]==276: #left
			self.LEFT = event.type==pygame.KEYDOWN and True or False
			#self.RIGHT = False
		elif event.dict["key"]==275: #right
			self.RIGHT = event.type==pygame.KEYDOWN and True or False
			#self.LEFT = False
		elif event.dict["key"]==32 and event.type==pygame.KEYDOWN: #space
			#print("Time left: ", self.timeUntilWeaponCanFireAgain);
				
			if self.timeUntilWeaponCanFireAgain <= 0:
				soundEfx = pygame.mixer.Sound(constants.BULLET_SFX)
				play_sound.PlaySounds(soundEfx)
				theBullet = bullet.Bullet((self.rect.x + SHIP_WIDTH/2 - bullet.BULLET_WIDTH/2, self.rect.y - (bullet.BULLET_HEIGHT + 6)))  # gets bullet far enough from ship
				# the following two lines are for classic arcade physics
				theBullet.v_x - 0
				theBullet.v_y = -bullet.DEFAULT_SPEED
				# the following two lines are for more real-world-type phsyics
				#theBullet.v_x = self.v_x
				#theBullet.v_y = self.v_y - bullet.DEFAULT_SPEED
				self.childObjects.append(theBullet)
				self.timeUntilWeaponCanFireAgain = GUN_COOLDOWN_TIME
		else:
			 handled_event = False

		return handled_event

