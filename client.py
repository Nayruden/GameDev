import socket
import sys
import pygame
import level
import tiles
import ship
import constants
import network
import pickle
from network import Message
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
theship = ship.Ship((constants.SCREEN_WIDTH/2, level.rect.height - 60), level, Rect(level.rect.x,level.rect.y,level.rect.width,constants.SCREEN_HEIGHT))

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
	theship.step(scrollPosition)
	screen.blit(theship.image, Rect((theship.rect.x, theship.rect.y - scrollPosition),(theship.rect.width, theship.rect.height)), theship.area)

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
		elif message == Message.SHIPSYNC:
			theship.r_x, theship.r_y, theship.v_x, theship.v_y = struct.unpack( "ffff", network.receiveData( conn ) )

		message = network.receiveIntData( conn, True )

	#movedlevelrect = movedlevelrect.move(0,SCROLL_RATE)

conn.close()
