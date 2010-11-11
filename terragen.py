
# creates randomly generated map

from __future__ import division
from random import random
from Perlin import PerlinGrid

class Biomes:
	Ocean = 0
	Sand = 1
	Grass = 2
	Trees = 3
	Dirt = 4
	Hill = 5
	Gap = 6
	Mountain = 7
	Snow = 8
	

BiomeGrid = [
	#low							#high
	[Biomes.Trees,	Biomes.Trees,	Biomes.Trees,	Biomes.Dirt,	Biomes.Gap,	Biomes.Gap,	Biomes.Snow,	Biomes.Snow	],	#wet
	[Biomes.Trees,	Biomes.Trees,	Biomes.Trees,	Biomes.Dirt,	Biomes.Hill,	Biomes.Hill,	Biomes.Snow,	Biomes.Snow	],	
	[Biomes.Grass,	Biomes.Grass,	Biomes.Grass,	Biomes.Dirt,	Biomes.Hill,	Biomes.Hill,	Biomes.Snow,	Biomes.Snow	],	
	[Biomes.Grass,	Biomes.Grass,	Biomes.Grass,	Biomes.Dirt,	Biomes.Hill,	Biomes.Hill,	Biomes.Mountain,	Biomes.Mountain	],	
	[Biomes.Grass,	Biomes.Grass,	Biomes.Grass,	Biomes.Dirt,	Biomes.Hill,	Biomes.Hill,	Biomes.Mountain,	Biomes.Mountain	],	
	[Biomes.Grass,	Biomes.Grass,	Biomes.Grass,	Biomes.Dirt,	Biomes.Dirt,	Biomes.Hill,	Biomes.Mountain,	Biomes.Mountain	],	
	[Biomes.Sand,	Biomes.Sand,	Biomes.Sand,	Biomes.Sand,	Biomes.Dirt,	Biomes.Hill,	Biomes.Mountain,	Biomes.Mountain	],	
	[Biomes.Sand,	Biomes.Sand,	Biomes.Sand,	Biomes.Sand,	Biomes.Dirt,	Biomes.Hill,	Biomes.Mountain,	Biomes.Mountain	]	#dry
]

class Tile():
	
	global BiomeGrid
	
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.height = 0
		self.wetness = 0
		self.biome = Biomes.Ocean
	
	def CalcBiome(tile, waterLevel):
		
		if tile.height <= waterLevel:
			tile.biome = Biomes.Ocean
			return
		
		scaledHeight = (tile.height - waterLevel) / (1.0001-waterLevel)
		
		heightGroup = min(int(scaledHeight*8), 7)
		wetGroup = min(int(tile.wetness*8), 7)
		
		#print tile.height,scaledHeight,heightGroup
		
		tile.biome = BiomeGrid[wetGroup][heightGroup]
	
	def Neighbors(tile, map):
		for x,y in ((-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)):
			nx = tile.x + x
			ny = tile.y + y
			if nx >= 0 and nx < map.width and ny >= 0 and ny < map.height:
				yield map.grid[ny][nx]
	

class Map():
	
	def __init__(self, width, height, waterApproach):
		self.width = width
		self.height = height
		self.InitGrid(width, height)
		
		self.Normalize()
		self.Deform()
		self.Normalize()
		self.NormalizeWetness()
		
		self.waterLevel = self.CalcWaterLevel(waterApproach)
		self.ClassifyBiomes(self.waterLevel)
		
		self.LineWaterWithSand()
		self.CullEdge(Biomes.Trees, Biomes.Grass)
		self.CullEdge(Biomes.Gap, Biomes.Hill)
		self.CullEdge(Biomes.Snow, Biomes.Mountain)
	
	
	def InitGrid(self, width, height):
		
		#perlinSpaceL = PerlinGrid(width, height, width/53, height/53)
		#perlinSpace = PerlinGrid(width, height, width/13, height/13)
		perlinSpaceH = PerlinGrid(width, height, width/7, height/7)
		
		perlinSpaceRain = PerlinGrid(width, height, width/21, height/15)
		
		self.grid = []
		
		for y in range(height):
			row = []
			for x in range(width):
				
				tile = Tile(x, y)
				
				#noise = perlinSpaceL.get(x,y)/2 +  perlinSpace.get(x,y)/4 + perlinSpaceH.get(x,y)/8
				noise = perlinSpaceH.get(x,y)
				
				tile.height = noise
				tile.wetness = (perlinSpaceRain.get(x,y)+1)/2
				
				row.append(tile)
				
			self.grid.append(row)
	
	
	def Normalize(map):
		
		min = 1.0
		max = -1.0
		
		for row in map.grid:
			for tile in row:
				if tile.height < min:
					min = tile.height
				if tile.height > max:
					max = tile.height
		
		scale = 1/(max - min)
		
		for row in map.grid:
			for tile in row:
				heightIndex = (tile.height - min) * scale
				tile.height = heightIndex
		
	
	
	def NormalizeWetness(map):
		
		min = 1.0
		max = -1.0
		
		for row in map.grid:
			for tile in row:
				if tile.wetness < min:
					min = tile.wetness
				if tile.wetness > max:
					max = tile.wetness
		
		scale = 1/(max - min)
		
		for row in map.grid:
			for tile in row:
				tile.wetness = (tile.wetness - min) * scale
	
	
	def Deform(map):
		
		for row in map.grid:
			for tile in row:
				falloff = (map.height - tile.y)/map.height
				
				falloff = 1-abs(2*falloff - 1)
				
				h = tile.height
				
				h = h*(falloff+1) + falloff
				h = h**2
				
				tile.height = h
		
	
	
	def ClassifyBiomes(map, waterLevel):
		
		for row in map.grid:
			for tile in row:
				tile.CalcBiome(waterLevel)
	
	
	def CalcWaterLevel(map, approach):
		
		maxLevel = 0
		
		for row in range(map.height - approach, map.height):
			for col in range(0, map.width):
				
				tile = map.grid[row][col]
				
				if(tile.height > maxLevel):
					maxLevel = tile.height
		
		return maxLevel
	
	def LineWaterWithSand(map):
		
		for row in map.grid:
			for tile in row:
				
				if tile.biome not in (Biomes.Grass, Biomes.Trees):
					continue
				
				byWater = False
				
				for neighbor in tile.Neighbors(map):
					if neighbor.biome == Biomes.Ocean:
						byWater = True
				
				if byWater is True:
					tile.biome = Biomes.Sand
	
	def CullEdge(map, centerBiome, edgeBiome):
		
		for row in map.grid:
			for tile in row:
				
				if tile.biome != centerBiome:
					continue
				
				edge = False
				
				for neighbor in tile.Neighbors(map):
					if neighbor.biome not in (centerBiome, edgeBiome):
						edge = True
				
				if edge:
					tile.biome = edgeBiome
	
	
