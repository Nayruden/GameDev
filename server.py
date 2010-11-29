import socket
import pickle
import pygame
import level
import tiles
import ship
import turret
import constants
import network
from network import Message
import struct

from pygame.rect import Rect

s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
s.bind( ('', constants.PORT) )
s.listen( 1 )
conn, addr = s.accept()
print 'Connection from', addr


screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)) #336, 432))
pygame.display.set_caption("Tyrian Defense SERVER")
clock = pygame.time.Clock()

level = level.Level()
physicalObjects = []
theship = ship.Ship((constants.SCREEN_WIDTH/2, level.rect.height - 60), level, Rect(level.rect.x,level.rect.y,level.rect.width,constants.SCREEN_HEIGHT))
physicalObjects.append(theship)

# sprinkle some targets across the map purely for testing physics
# this should be removed from the server code eventually
physicalObjects.append(turret.Turret((170, 4475)))
physicalObjects.append(turret.Turret((250, 4275)))
physicalObjects.append(turret.Turret((450, 4425)))

leveldata = pickle.dumps( level.terrian, constants.PROTOCOL )
network.sendData( conn, leveldata )

scrollPosition = level.rect.height - constants.SCREEN_HEIGHT

movedlevelrect = level.rect.move(0,-level.yoffset)
running = True

while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	if not theship.handle_event(event):
		pass #todo: handle events the ship isn't interested in

	for o in physicalObjects[:]:  # update all physical objects
		o.step(scrollPosition)  # update the object
		if(o.destroyed):
			physicalObjects.remove(o)  # remove destroyed objects from the universe
	for o1 in physicalObjects:  # collision-detection time!
		for o2 in physicalObjects:
			if o1 != o2:
				if o1.physicsRect.colliderect(o2.physicsRect):
					o1.resolveCollisionWith(o2)  # resolve collision by
					o2.resolveCollisionWith(o1)  #  destroying objects
	for o in physicalObjects[:]:  # add any new objects to the universe
		while len(o.childObjects) != 0:
			physicalObjects.append(o.childObjects.pop(0))

	screen.fill(pygame.Color('black'))
	movedlevelrect.y = -scrollPosition;
	screen.blit(level.image, movedlevelrect)
	for o in physicalObjects:
		# commented lines are for physics testing
		#screen.fill((255, 255, 255), Rect((o.rect.x, o.rect.y - scrollPosition),(o.rect.width, o.rect.height)))
		#screen.fill((255, 0, 0), Rect((o.physicsRect.x, o.physicsRect.y - scrollPosition), (o.physicsRect.width, o.physicsRect.height)))
		screen.blit(o.image, Rect((o.rect.x, o.rect.y - scrollPosition),(o.rect.width, o.rect.height)), o.area)

	pygame.display.flip()
	clock.tick(60)

	#scroll the level down
	scrollPosition -= constants.SCROLL_RATE
	#movedlevelrect = movedlevelrect.move(0,SCROLL_RATE)

	#Network:
	network.sendIntData( conn, Message.SCROLLSYNC )
	network.sendIntData( conn, scrollPosition )

	#Need to generalize this into any phys obj and come up with some ID system for the objs
	network.sendIntData( conn, Message.SHIPSYNC )
	network.sendData( conn, struct.pack( "ffff", theship.getX(), theship.getY(), theship.getVX(), theship.getVY() ) )

conn.close()
