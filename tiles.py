import pygame

class Tiles(pygame.rect.Rect):
	"""This class gives the area on the tilesheet for a given tile"""
	def __init__(self, tilecode):
		tsize = twidth, theight = 24, 28 #tile size
		
		# Tiles are named by what material they have in each corner:
		# 0 = GRASS  can only be next to DIRT and TREE
		# 1 = DIRT   can only be next to HILL and GRASS
		# 2 = HILL   can only be next to DIRT and MTN
		# 3 = MTN    can only be next to HILL
		# 4 = EMPTY  can only be next to HILL
		# 5 = TREE   can only be next to GRASS
		# 9 = CLOUD  can only be OVER anything       11
		# ** I would use clouds as a seperate layer with some alpha
		# So "1101" would refer to a tile like this: 01 or mostly dirt
		# with grass in the bottom left
		
		self.tiles = {  # Grass-Dirt Transition Tiles
				"0001":	(0*twidth, 0, twidth, theight),
		  		"0011":	(1*twidth, 0, twidth, theight),
				"0010":	(2*twidth, 0, twidth, theight),
				"0000":	(3*twidth, 0, twidth, theight),
				"0110":	(5*twidth, 0*theight, twidth, theight),	
				"0101":	(0*twidth, 1*theight, twidth, theight),
				"1111":	(1*twidth, 1*theight, twidth, theight),
				"1010":	(2*twidth, 1*theight, twidth, theight),
				"0111":	(3*twidth, 1*theight, twidth, theight),
				"1011":	(4*twidth, 1*theight, twidth, theight),
				"1001":	(5*twidth, 1*theight, twidth, theight),
				"0100":	(0*twidth, 2*theight, twidth, theight),
				"1100":	(1*twidth, 2*theight, twidth, theight),
				"1000":	(2*twidth, 2*theight, twidth, theight),
				"1101":	(3*twidth, 2*theight, twidth, theight),
				"1110":	(4*twidth, 2*theight, twidth, theight),
				# Grass-Tree Transition Tiles	
				"0002":	(0*twidth, 3*theight, twidth, theight),
		  		"0022":	(1*twidth, 3*theight, twidth, theight),
				"0020":	(2*twidth, 3*theight, twidth, theight),
				"2222":	(4*twidth, 3*theight, twidth, theight),
				"0220":	(5*twidth, 3*theight, twidth, theight),	
				"0202":	(0*twidth, 4*theight, twidth, theight),
				"2222":	(1*twidth, 4*theight, twidth, theight),
				"2020":	(2*twidth, 4*theight, twidth, theight),
				"0222":	(3*twidth, 4*theight, twidth, theight),
				"2022":	(4*twidth, 4*theight, twidth, theight),
				"2002":	(5*twidth, 4*theight, twidth, theight),
				"0200":	(0*twidth, 5*theight, twidth, theight),
				"2200":	(1*twidth, 5*theight, twidth, theight),
				"2000":	(2*twidth, 5*theight, twidth, theight),
				"2202":	(3*twidth, 5*theight, twidth, theight),
				"2220":	(4*twidth, 5*theight, twidth, theight),
				# Sand-Water1 Tiles (sand = 3; water = 4)
				"3334":	(0*twidth, 21*theight, twidth, theight),
		  		"3344":	(1*twidth, 21*theight, twidth, theight),
				"3343":	(2*twidth, 21*theight, twidth, theight),
				"3333":	(5*twidth, 21*theight, twidth, theight),
				"3443":	(5*twidth, 23*theight, twidth, theight),	
				"3434":	(0*twidth, 22*theight, twidth, theight),
				"4444":	(1*twidth, 22*theight, twidth, theight),
				"4343":	(2*twidth, 22*theight, twidth, theight),
				"3444":	(4*twidth, 22*theight, twidth, theight),
				"4344":	(3*twidth, 22*theight, twidth, theight),
				"4334":	(5*twidth, 22*theight, twidth, theight),
				"3433":	(0*twidth, 23*theight, twidth, theight),
				"4433":	(1*twidth, 23*theight, twidth, theight),
				"4333":	(2*twidth, 23*theight, twidth, theight),
				"4434":	(4*twidth, 21*theight, twidth, theight),
				"4443":	(3*twidth, 21*theight, twidth, theight)
				
			}
		
		self.area = pygame.rect.Rect(self.tiles[tilecode])