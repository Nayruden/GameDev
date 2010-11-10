import pygame
import tiles

class World(object):
	def __init__(self):
		
		#tiles = tiles.Tiles((250, 355), world)
		
		self.image = pygame.image.load("images/blank.gif")
		self.rect = self.image.get_rect()
		
		
		self.solids = [	[-10, 290, 355], # used for mario platforms
				[70, 165, 291],
				[38, 120, 228],
				[70, 149, 164],
				[119, 216, 116],
				[259, 336, 132] ]
