import pygame
import tiles
import random
import terragen
import constants

class Level(object):

	# instance varaibles
	physicalObjects = []
	physicalObjectsExternalRemoveList = []  # used to inform other entities that objects have been destroyed/deleted
	# note: physicalObjectsExternalRemoveList was intended to be emptied at the beginning of each step

	def __init__(self, terrian = None):
		if terrian is None:
			cols = constants.COLS # we want 26 cols of tiles to cover a width of 624
			rows = constants.ROWS # we want 18 rows of tiles to cover a height of 480

			# I don't know of a better way to initialize that works
			self.terrian = []#[[0 for row in range(rows+1)] for col in range(cols+1)]

			map = terragen.Map(cols+1,rows+1,18)

			# creates a random array
			for col in range (0,cols+1):
				newCol = []
				for row in range (0,rows+1):
					newCol.append(map.grid[row][col].biome)
				self.terrian.append(newCol)

		else:
			self.terrian = terrian

		"""
		# prints my array to the console (DEBUG)
		for row in terrian:
			print row
		"""

		self.generateImage()


	def generateImage(self):
		#image from which all tiles are pulled
		tilesheet = pygame.image.load('images/tiles.png')

		tsize = twidth, theight = 24,28 # each tile is 24x28

		#self.image = pygame.image.load("images/blank.gif") # bg image
		self.image = pygame.Surface( (624, 5040) ) # instead of bg image

		for col in range (0,constants.COLS):
			for row in range (0,constants.ROWS):
				location = 0+col*twidth,0+row*theight, twidth, theight
				tilestring = "" + str(self.terrian[col][row])+str(self.terrian[col+1][row])+str(self.terrian[col][row+1])+str(self.terrian[col+1][row+1])
				#print tilestring # for debug
				self.image.blit(tilesheet, location, tiles.Tiles(tilestring).area )


		self.rect = self.image.get_rect()

		self.yoffset = constants.ROWS*theight - 480


	def step(self, scrollPosition):
		self.physicalObjectsExternalRemoveList[:] = []  # empty the list of objects destroyed in the last step
		for o in self.physicalObjects[:]:  # update all physical objects
			o.step(scrollPosition)  # update the object
			if(o.destroyed):
				self.physicalObjectsExternalRemoveList.append(o);
				self.physicalObjects.remove(o)  # remove destroyed objects from the universe
		for o1 in self.physicalObjects:  # collision-detection time!
			for o2 in self.physicalObjects:
				if o1 != o2:
					if o1.physicsRect.colliderect(o2.physicsRect):
						o1.resolveCollisionWith(o2)
						o2.resolveCollisionWith(o1)
		for o in self.physicalObjects[:]:  # add any new objects to the universe
			while len(o.childObjects) != 0:
				self.physicalObjects.append(o.childObjects.pop(0))
