
from __future__ import division
import terragen, pygame, sys;

Biomes = terragen.Biomes

pygame.init()

w = 64//3
h = 64*2
squareSize = 7
approach = 30

screenWidth = w*squareSize
screenHeight = h*squareSize
screen = pygame.display.set_mode( (screenWidth,screenHeight) );

mousePos = None

def Main():
	global mousePos
	
	map = terragen.Map(w, h, approach//squareSize)
	
	#DrawMap(map, 0,(0,screenHeight+1))
	
	mousePos = (0,0)
	
	while True:
		ProcessEvents()
		
		if mousePos:
			
			left = max(0, mousePos[0] - 8)
			right = min( mousePos[0] + 8, screenWidth)
			top = mousePos[1]
			
			#waterLevel = CalcWaterLevel(map, left//squareSize, right//squareSize, top//squareSize)
			#waterLevel = CalcWaterLevel(map, 0, screenWidth//squareSize, (screenHeight-approach)//squareSize)
			
			#DrawMap(map, 1-(mousePos[1]/screenHeight), mousePos)
			#terragen.ClassifyBiomes(map, waterLevel)
			DrawMap(map, mousePos)
			mousePos = None
			
			screen.fill((128,0,255), ((0,screenHeight-approach), (screenWidth,2)))
			#screen.fill((128,0,255), ((left,top), (right-left,2)))
			#screen.fill((128,0,255), ((left,top), (2,screenHeight-top)))
			#screen.fill((128,0,255), ((right-2,top), (2,screenHeight-top)))
			
			pygame.display.flip()


def DrawMap(map, mousePos):
	
	global screenWidth
	
	for row in map.grid:
		for tile in row:
			
			if tile.biome == Biomes.Ocean:
				color = (0,255-(map.waterLevel-tile.height)*255,255)
			elif tile.biome == Biomes.Sand:
				color = (255,255,200)
			elif tile.biome == Biomes.Trees:
				color = (0,200,0)
			elif tile.biome == Biomes.Dirt:
				color = (128,64,0)
			elif tile.biome == Biomes.Rock:
				color = (128,128,128)
			else:
				color = (128,128,128)
			
			screen.fill(color, ((tile.x*squareSize, tile.y*squareSize), (squareSize,squareSize)))
		
	

def ProcessEvents():
	global mousePos
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.MOUSEMOTION:
			mousePos = event.pos
			#waterLevel = 1-(event.pos[1]/(h*squareSize))

Main()
