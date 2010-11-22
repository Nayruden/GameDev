import pygame

class Tiles(pygame.rect.Rect):
	"""This class gives the area on the tilesheet for a given tile"""
	def __init__(self, tilecode):
		tsize = twidth, theight = 24, 28 #tile size
		
		# STILL WORKING ON; 3-1 7-8 7-9
		
		# Tiles are named by what material they have in each corner:
		# 
		# ** I would use clouds as a seperate layer with some alpha
		# So "1101" would refer to a tile like this: 01 or mostly dirt
		# with grass in the bottom left
		
		# Set 0: GRASS-DIRT (already configured)
		# The default transition set is the part of the image that has
		tset = 0  # conversions from grass to dirt (0-1)
		
		# Now I adapt the tilecodes to be part of a given transition set
		# this means changing something like 3343 to 0010,
		#  and saying that we are in tileset 6 (that is where the 3-4s are)
		
		# Set 1: TREE-GRASS set: right now 2 (tree) only happens in grass (0)
		if "2" in tilecode: # so change those 2's to 1's for pattern matching
			tilecode = tilecode.replace("2", "1")
			tset = 1 # but change the transition set
		
		# Set 2: DIRT-HILL 
		if "1" in tilecode: 
			if "5" in tilecode:# and ("0" in tilecode == False):
				tilecode = tilecode.replace("0", "G") # grass fix
				tilecode = tilecode.replace("5", "0")
				tset = 2
				
		# Set 3: HILL-MOUNTIAN
		if "5" in tilecode:
			if "7" in tilecode:
				tilecode = tilecode.replace("5", "0")
				tilecode = tilecode.replace("7", "1")
				tset = 3
		
		# Set 3: MOUNTIAN-LAVA
		if "7" in tilecode:
			if "9" in tilecode:
				tilecode = tilecode.replace("7", "0")
				tilecode = tilecode.replace("9", "1")
				tset = 4
				
		# Set 3: MOUNTIAN-ICE
		if "7" in tilecode:
			if "8" in tilecode:
				tilecode = tilecode.replace("7", "0")
				tilecode = tilecode.replace("8", "1")
				tset = 4
		
		
		# sets with water
		if "4" in tilecode:
			if "3" in tilecode: # the set for sand-water
				tilecode = tilecode.replace("3", "0")
				tilecode = tilecode.replace("4", "1")
				tset = 6
			elif "A" in tilecode: # the set for water-deepwater
				tilecode = tilecode.replace("4", "0")
				tilecode = tilecode.replace("A", "1")
				tset = 8
				
		# Set 7: GRASS-SAND
		if "3" in tilecode:
			if "0" in tilecode:
				tilecode = tilecode.replace("1", "D") # dirt fix
				tilecode = tilecode.replace("3", "1")
				tset = 7
				
		# Pure tile fix: alternatively I could hardcode them into self.tiles
		#  or figure out my logic better so these resolve in set translation
		if tilecode == "3333":
			tilecode = "0000" # this covers pure sand
			tset = 6
		if tilecode == "4444":
			tilecode = "1111" # this covers pure water
			tset = 6
		if tilecode == "5555":
			tilecode = "0000" # this covers pure hill
			tset = 2
		if tilecode == "7777" in tilecode: # covers pure deepwater
			tilecode = "1111"
			tset = 3
		if tilecode == "8888" in tilecode: # covers pure deepwater
			tilecode = "1111"
			tset = 4
		if tilecode == "9999" in tilecode: # covers pure deepwater
			tilecode = "1111"
			tset = 4
		if tilecode == "AAAA" in tilecode: # covers pure deepwater
			tilecode = "0000"
			tset = 8
		
		self.tiles = {  # Base Transition Tile Locations for a given Transition Set
				"0001":	(0*twidth, (0+3*tset)*theight, twidth, theight),
		  		"0011":	(1*twidth, (0+3*tset)*theight, twidth, theight),
				"0010":	(2*twidth, (0+3*tset)*theight, twidth, theight),
				"0000":	(3*twidth, (0+3*tset)*theight, twidth, theight),
				"0110":	(5*twidth, (0+3*tset)*theight, twidth, theight),	
				"0101":	(0*twidth, (1+3*tset)*theight, twidth, theight),
				"1111":	(1*twidth, (1+3*tset)*theight, twidth, theight),
				"1010":	(2*twidth, (1+3*tset)*theight, twidth, theight),
				"0111":	(3*twidth, (1+3*tset)*theight, twidth, theight),
				"1011":	(4*twidth, (1+3*tset)*theight, twidth, theight),
				"1001":	(5*twidth, (1+3*tset)*theight, twidth, theight),
				"0100":	(0*twidth, (2+3*tset)*theight, twidth, theight),
				"1100":	(1*twidth, (2+3*tset)*theight, twidth, theight),
				"1000":	(2*twidth, (2+3*tset)*theight, twidth, theight),
				"1101":	(3*twidth, (2+3*tset)*theight, twidth, theight),
				"1110":	(4*twidth, (2+3*tset)*theight, twidth, theight)
			}
		
		if tilecode in self.tiles:
			self.area = pygame.rect.Rect(self.tiles[tilecode])
		else:
			print tilecode
			self.area = pygame.rect.Rect((0*twidth, 0*theight, twidth/2, theight/2))