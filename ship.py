#!/usr/bin/env python
import pygame


#for AWESOME input!!! (fixing pygame's b0rked event handling)



class Ship(pygame.sprite.Sprite):
	"""This class represents the ship"""
        v_x = 0.0
        v_y = 0.0
        LEFT = False
        RIGHT = False
        UP = False
        DOWN = False

	def __init__(self, position, level,level_actual_rect):
		pygame.sprite.Sprite.__init__(self)
		self.level = level
		
		self.image = pygame.image.load('images/ship.png')
		self.rect = self.image.get_rect()
		
		self.actions = {	"center":			(46*2,0,46,50),
                                        "left":                         (46*0,0,46,50),
                                        "left-center":                  (46*1,0,46,50),
                                        "right-center":                 (46*3,0,46,50),
                                        "right":                        (46*4,0,46,50)                                         
				}
		
		self.action = "center"
		self.area = pygame.rect.Rect(self.actions[self.action])
		self.rect.topleft = position
                self.level_actual_rect = level_actual_rect
        
        def step(self):
            #tight physics
            v_step = 0.5
            v_target = 6.0
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
 
            #update position
            self.rect.x += self.v_x
            self.rect.y += self.v_y
            
            #hard bounds fix
            if self.rect.x + self.area.width > self.level_actual_rect.width:
                self.rect.x = self.level_actual_rect.width - self.area.width
            if self.rect.x < 0:
                self.rect.x = 0
            if self.rect.y + self.area.height > self.level_actual_rect.height:
                self.rect.y = self.level_actual_rect.height - self.area.height
            if self.rect.y < 0:
                self.rect.y = 0
                
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
            else:
                handled_event = False
            
            
            
            return handled_event
