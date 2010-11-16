import pygame
import tiles
import random
import terragen

class Level(object):
	def __init__(self):
		#image from which all tiles are pulled
		tilesheet = pygame.image.load('images/tiles.png')
		
		tsize = twidth, theight = 24,28 # each tile is 24x28
		
		cols = 26 # we want 26 cols of tiles to cover a width of 624
		rows = 180 # we want 18 rows of tiles to cover a height of 480
		
		self.yoffset = rows*theight - 480
		
		# I don't know of a better way to initialize that works
		terrian = []#[[0 for row in range(rows+1)] for col in range(cols+1)]
		
		map = terragen.Map(cols+1,rows+1,18)
		
		# creates a random array
		for col in range (0,cols+1):
			newCol = []
			for row in range (0,rows+1):
				newCol.append(map.grid[row][col].biome)
			terrian.append(newCol)
		
		"""
		# prints my array to the console (DEBUG)
		for row in terrian:
			print row
		"""
		
		
		
		#self.image = pygame.image.load("images/blank.gif") # bg image
		self.image = pygame.Surface( (624, 5040) ) # instead of bg image
		
		for col in range (0,cols):
			for row in range (0,rows):
				location = 0+col*twidth,0+row*theight, twidth, theight
				tilestring = "" + str(terrian[col][row])+str(terrian[col+1][row])+str(terrian[col][row+1])+str(terrian[col+1][row+1])
				#print tilestring # for debug
				self.image.blit(tilesheet, location, tiles.Tiles(tilestring).area )
				
		
		self.rect = self.image.get_rect()
		
		
		self.solids = [	[-10, 290, 355], # used for mario platforms
				[70, 165, 291],
				[38, 120, 228],
				[70, 149, 164],
				[119, 216, 116],
				[259, 336, 132] ]
