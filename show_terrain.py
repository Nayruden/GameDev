
# tests terrain generator

from __future__ import division
import terragen, pygame, sys;

Biomes = terragen.Biomes

pygame.init()

w = 21
h = 110
squareSize = 7
approach = 30

screenWidth = w*squareSize
screenHeight = h*squareSize
screen = pygame.display.set_mode( (screenWidth,screenHeight) );

def Main():
	
	map = terragen.Map(w, h, approach//squareSize)
	
	DrawMap(map)
	
	screen.fill((128,0,255), ((0,screenHeight-approach), (screenWidth,2)))
	
	pygame.display.flip()
	
	while True:
		ProcessEvents()
	


def DrawMap(map):
	
	for row in map.grid:
		for tile in row:
			
			if tile.biome == Biomes.Ocean:
				color = (0,255-(map.waterLevel-tile.height)*255,255)
			elif tile.biome == Biomes.Sand:
				color = (255,255,200)
			elif tile.biome == Biomes.Grass:
				color = (0,255,0)
			elif tile.biome == Biomes.Trees:
				color = (0,200,0)
			elif tile.biome == Biomes.Dirt:
				color = (128,64,0)
			elif tile.biome == Biomes.Hill:
				color = (100,60,20)
			elif tile.biome == Biomes.Gap:
				color = (0,0,0)
			elif tile.biome == Biomes.Mountain:
				color = (128,128,128)
			elif tile.biome == Biomes.Snow:
				color = (255,255,255)
			else:
				color = (255,0,255)
			
			screen.fill(color, ((tile.x*squareSize, tile.y*squareSize), (squareSize,squareSize)))
		
	

def ProcessEvents():
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

Main()
