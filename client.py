import socket
import sys
import pygame
import level
import tiles
import ship
import constants
import turret
import bullet
import network
import pickle
from network import Message
from network import Type
import math
import struct

from pygame.rect import Rect
from pygame import mixer
from pygame.mixer import Sound

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect((sys.argv[-1], constants.PORT))

screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)) #336, 432))
pygame.display.set_caption("Tyrian Defense CLIENT")
clock = pygame.time.Clock()

packed = network.receiveData( conn )
leveldata = pickle.loads( packed )
level = level.Level( leveldata )
#theship = ship.Ship((constants.SCREEN_WIDTH/2, level.rect.height - 60), level)

physicalObjects = {}

scrollPosition = level.rect.height - constants.SCREEN_HEIGHT

movedlevelrect = level.rect.move(0,-level.yoffset)
running = True

# sound on two channels, both at start of game
pygame.mixer.init(44100,-16,16, 1024)
background = pygame.mixer.Sound("sounds/background/background.ogg")
danger = pygame.mixer.Sound("sounds/dangerWarning.ogg")
danger.set_volume(1.0)
background.set_volume(0.3)
channelBackground = pygame.mixer.find_channel()
channelBackground.play(background)
channelExtra = pygame.mixer.find_channel() #locate chanel w/o any sound on it
channelExtra.play(danger)

while running:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	screen.fill(pygame.Color('black'))
	movedlevelrect.y = -scrollPosition;
	screen.blit(level.image, movedlevelrect)

	for i, o in physicalObjects.iteritems():
		o.step(scrollPosition)
		screen.blit(o.image, Rect((o.rect.x, o.rect.y - scrollPosition),(o.rect.width, o.rect.height)), o.area)

	pygame.display.flip()
	clock.tick(60)

	scrollPosition -= constants.SCROLL_RATE

	#Network:
	message = network.receiveIntData( conn, True )
	while message != None:
		message, = message
		if message == Message.SCROLLSYNC:
			scrollPositionTarget, = network.receiveIntData( conn )
			if math.fabs( scrollPosition - scrollPositionTarget ) > 10: # Can't be off by more than this amount
				scrollPosition = scrollPositionTarget
		elif message == Message.NEWOBJ:
			typ, netid = struct.unpack( "ii", network.receiveData( conn ) )
			obj = None
			if typ == Type.SHIP:
				obj = ship.Ship((0,0), level)
			elif typ == Type.TURRET:
				obj = turret.Turret((0,0))
			elif typ == Type.BULLET:
				obj = bullet.Bullet((0,0))
			physicalObjects[ netid ] = obj
		elif message == Message.OBJSYNC:
			netid, x, y, vx, vy = struct.unpack( "iffff", network.receiveData( conn ) )
			obj = physicalObjects[ netid ]
			obj.setX( x )
			obj.setY( y )
			obj.v_x, obj.v_y = (vx, vy)
		elif message == Message.DESTROYOBJ:
			netid, = network.receiveIntData( conn )
			if netid in physicalObjects:
				del physicalObjects[ netid ]

		message = network.receiveIntData( conn, True )

	#movedlevelrect = movedlevelrect.move(0,SCROLL_RATE)

conn.close()
