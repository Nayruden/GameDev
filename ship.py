#!/usr/bin/env python
import pygame
import constants
from physical_object import PhysicalObject
import bullet

#for AWESOME input!!! (fixing pygame's b0rked event handling)

GUN_COOLDOWN_TIME = 10


class Ship(PhysicalObject):
	"""This class represents the ship"""

	timeUntilWeaponCanFireAgain = 0


	def __init__(self, position, level,level_actual_rect):

		PhysicalObject.__init__(self, position)
		self.level = level
		
		self.image = pygame.image.load('images/ship.png')
		self.rect = self.image.get_rect()
		
		self.actions = {	"center":	(46*2,0,46,50),
			"left":	 (46*0,0,46,50),
			"left-center":	(46*1,0,46,50),
			"right-center":	(46*3,0,46,50),
			"right":	(46*4,0,46,50)                                         
			}
		
		self.action = "center"
		self.area = pygame.rect.Rect(self.actions[self.action])

		self.level_actual_rect = level_actual_rect

		self.physicsRect = pygame.rect.Rect(self.r_x, self.r_y, 46, 50)
		
	def step(self, scrollPosition):
			#tight physics
			v_step = 0.5
			v_target = 6.0

			# determine speed
			def towards(current,expected):
				if abs(expected-current) < v_step: return expected
				if current > expected:
					return current - v_step
				return current + v_step
				
			if self.DOWN and not self.UP:
				self.v_y = towards(self.v_y,v_target)
			elif self.UP and not self.DOWN:
				self.v_y = towards(self.v_y,-v_target)
			elif not self.UP and not self.DOWN:
				self.v_y = towards(self.v_y,0)
			if self.LEFT and not self.RIGHT:
				self.v_x = towards(self.v_x,-v_target)
			elif self.RIGHT and not self.LEFT:
				self.v_x = towards(self.v_x,v_target)
			elif not self.LEFT and not self.RIGHT:
				self.v_x = towards(self.v_x,0)

			# update position
			PhysicalObject.step(self, scrollPosition)
			
			#hard bounds fix
			if self.physicsRect.x + self.physicsRect.width > self.level_actual_rect.width:
				self.setX(self.level_actual_rect.width - self.physicsRect.width)
			if self.r_x < 0:
				self.setX(0)
			if self.r_y + self.physicsRect.height > scrollPosition + constants.SCREEN_HEIGHT:
				self.setY(scrollPosition + constants.SCREEN_HEIGHT - self.physicsRect.height)
			if self.r_y < scrollPosition:
				self.setY(scrollPosition)
			
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
				theBullet = bullet.Bullet((self.rect.x, self.rect.y - 40))  # 40 gets bullet far enough from ship
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
		
