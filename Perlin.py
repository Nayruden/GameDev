
# Perlin noise module

from random import random
from math import sqrt, ceil

class PerlinGrid():
	def __init__(self, width, height, vectorWidth, vectorHeight):
		self.width = width
		self.height = height
		self.xScale = vectorWidth / (width + 1)
		self.yScale = vectorHeight / (height + 1)
		
		self.grid = genPerlinVectorGrid(int(ceil(vectorWidth+1)), int(ceil(vectorHeight+1)))
	
	def get(self,x,y):
		scaledX, scaledY = x*self.xScale, y*self.yScale
		intX, intY = int(scaledX), int(scaledY)
		
		upperLeft = influence(self.grid[intY][intX], intX, intY, scaledX, scaledY)
		upperRight = influence(self.grid[intY][intX+1], intX+1, intY, scaledX, scaledY)
		lowerLeft = influence(self.grid[intY+1][intX], intX, intY+1, scaledX, scaledY)
		lowerRight = influence(self.grid[intY+1][intX+1], intX+1, intY+1, scaledX, scaledY)
		
		upper = cubicInterpolate(upperLeft, upperRight, scaledX - intX)
		lower = cubicInterpolate(lowerLeft, lowerRight, scaledX - intX)
		
		value = cubicInterpolate(upper, lower, scaledY - intY)
		
		return value

def genPerlinVectorGrid(width, height):
	
	grid = []
	
	for y in range(height):
		row = []
		for x in range(width):
			row.append(genPerlinVector())
		grid.append(row)
	
	return grid

def genPerlinVector():
	vector = (random()*2 - 1, random()*2 - 1)
	lengthSquared = vector[0]**2 + vector[1]**2
	while lengthSquared > 1.0:
		vector = (random()*2 - 1, random()*2 - 1)
		lengthSquared = vector[0]**2 + vector[1]**2
	
	return normalize(vector)

def influence(vector, vx, vy, ix, iy):
	diff = ( ((vx-ix), (vy-iy)) )
	dotP = vector[0]*diff[0] + vector[1]*diff[1]
	return dotP

def normalize(vector):
	length = sqrt(vector[0]**2 + vector[1]**2)
	if length == 0:
		return (0,0)
	return (vector[0]/length, vector[1]/length)

def linearInterpolate(a,b, i):
	return (1-i)*a + i*b

def cubicInterpolate(a,b, i):
	return a - (3*i**2 - 2*i**3)*(a-b)
