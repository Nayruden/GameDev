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
import play_sound
from network import Message
from network import Type
import math
import struct

from pygame.rect import Rect
from pygame import mixer
from pygame.mixer import Sound

screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Tyrian Defense CLIENT")

introscreen = pygame.image.load('images/pyrian.png')
screen.blit(introscreen, introscreen.get_rect())

# Display some text
pygame.font.init()
arial = pygame.font.match_font('doesNotExist,Arial')
font = pygame.font.Font(arial, 36)
text = font.render("Press any key to start", 1, (10, 10, 10))
textpos = text.get_rect()
textpos.centerx = screen.get_rect().centerx
screen.blit(text, textpos)

pygame.display.flip()

# Wait for a key to be pressed
while (pygame.event.wait().type != pygame.KEYDOWN): pass

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect((sys.argv[-1], constants.PORT))

clock = pygame.time.Clock()

packed = network.receiveData( conn )
leveldata = pickle.loads( packed )
level = level.Level( leveldata )
theship = None

physicalObjects = {}

scrollPosition = level.rect.height - constants.SCREEN_HEIGHT

movedlevelrect = level.rect.move(0,-level.yoffset)
running = True

while running:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.KEYDOWN and event.dict["key"]==32:
			obj = turret.Turret((theship.r_x,theship.r_y - 400),level)
			from random import choice
			#this is really a terrible idea...
			physicalObjects[choice(range(99999))] = obj

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
				obj = theship = ship.Ship((0,0), level)
			elif typ == Type.TURRET:
				obj = turret.Turret((0,0), level)
			elif typ == Type.TBULLET:
				obj = bullet.Bullet((0,0), "tur")
			elif typ == Type.SBULLET:
				obj = bullet.Bullet((0,0), "shp")
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
