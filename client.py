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

# used if game is on mulitple machines...if on the same machine,
# the two programs' sounds will overlap and not sound good
startSFX = pygame.mixer.Sound(constants.START_MUSIC)
startSFX.set_volume(0.7)
endSFX = pygame.mixer.Sound(constants.END_MUSIC)
endSFX.set_volume(0.7)
backgroundSFX = pygame.mixer.Sound(constants.BACKGROUND_MUSIC)
backgroundSFX.set_volume(0.5)

screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Tyrian Defense CLIENT")

introscreen = pygame.image.load('images/pyrian.png')
pygame.time.wait(15)
# another for multiple machines
play_sound.PlaySounds(startSFX, 0)
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

lastNetworkID = 1 # client uses odd ids
physicalObjects = {}

scrollPosition = level.rect.height - constants.SCREEN_HEIGHT

movedlevelrect = level.rect.move(0,-level.yoffset)
running = True

PLACEMENT_COOLDOWN_TIME = 90 # may be too high
turretPlacementClock = 0

lastID = 1 # Client will assign odd-numbered netids
# for two machines
play_sound.PlaySounds(backgroundSFX, 1)

while running:

	if turretPlacementClock > 0:
		turretPlacementClock -= 1

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and turretPlacementClock == 0:
			pos = pygame.mouse.get_pos()
			obj = turret.Turret((-movedlevelrect.x+pos[0],-movedlevelrect.y+pos[1]),level)
			print pos
			print movedlevelrect
			turretPlacementClock = PLACEMENT_COOLDOWN_TIME
			lastNetworkID = lastNetworkID + 2
			physicalObjects[lastNetworkID] = obj
			network.sendIntData( conn, Message.NEWOBJ )
			network.sendData( conn, struct.pack( "ii", Type.TURRET, lastNetworkID ) )
			network.sendIntData( conn, Message.OBJSYNC )
			network.sendData( conn, struct.pack( "iffff", lastNetworkID, obj.getX(), obj.getY(), obj.getVX(), obj.getVY() ) )

	screen.fill(pygame.Color('black'))
	movedlevelrect.y = -scrollPosition;
	screen.blit(level.image, movedlevelrect)

	for i, o in physicalObjects.iteritems():
		o.step(scrollPosition)
		screen.blit(o.image, Rect((o.rect.x, o.rect.y - scrollPosition),(o.rect.width, o.rect.height)), o.area)



	#if not at the end of the level, update the display and scroll the level down
	if scrollPosition != 0:
		pygame.display.flip()
		clock.tick(60)
		scrollPosition -= constants.SCROLL_RATE
	else:
		losescreen = pygame.image.load('images/lose.png')
		screen.blit(losescreen, losescreen.get_rect())
		pygame.display.flip()
		

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
