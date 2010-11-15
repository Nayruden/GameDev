#!/usr/bin/env python
import pygame
class Ship(pygame.sprite.Sprite):
	"""This class represents the ship"""
	def __init__(self, position, level):
		pygame.sprite.Sprite.__init__(self)
		self.level = level
		
		self.image = pygame.image.load('images/ship.png')
		self.rect = self.image.get_rect()
		
		self.actions = {	"center":			(45*2,0,45,50),
                                        "left":                         (45*0,0,45,50),
                                        "left-center":                  (45*1,0,45,50),
                                        "right-center":                 (45*3,0,45,50),
                                        "right":                        (45*4,0,45,50)                                         
				}
		
		self.action = "center"
		self.area = pygame.rect.Rect(self.actions[self.action])
		self.rect.topleft = position
        def handle_event(self,event):
            pass
