import socket
import pickle
import pygame
import level
import tiles
import physical_object
import ship
import turret
import constants
import network
from network import Message
import struct

from pygame.rect import Rect

import play_sound
from pygame import mixer
from pygame.mixer import Sound
#from pygame import font

# ready the display
screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Tyrian Defense SERVER")

# load introscreen
introscreen = pygame.image.load('images/pyrian.png')
screen.blit(introscreen, introscreen.get_rect())

# Display some text
pygame.font.init()
arial = pygame.font.match_font('doesNotExist,Arial')
font = pygame.font.Font(arial, 36)
text = font.render("Waiting for client", 1, (10, 10, 10))
textpos = text.get_rect()
textpos.centerx = screen.get_rect().centerx
screen.blit(text, textpos)


pygame.display.flip()

s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
s.bind( ('', constants.PORT) )
s.listen( 1 )
conn, addr = s.accept()
print 'Connection from', addr

clock = pygame.time.Clock()

level = level.Level()
removeQueue = []
lastNetworkID = 0
physical_object.init(True)
theship = ship.Ship((constants.SCREEN_WIDTH/2, level.rect.height - 60), level)
level.physicalObjects.append(theship)

# sprinkle some targets across the map purely for testing physics
# this should be removed from the server code eventually
level.physicalObjects.append(turret.Turret((170, 4475), level))
level.physicalObjects.append(turret.Turret((250, 4275), level))
level.physicalObjects.append(turret.Turret((450, 4425), level))

leveldata = pickle.dumps( level.terrian, constants.PROTOCOL )
network.sendData( conn, leveldata )

scrollPosition = level.rect.height - constants.SCREEN_HEIGHT

movedlevelrect = level.rect.move(0,-level.yoffset)
running = True

# create the background music and send it to the class to play the sounds
sounds = pygame.mixer.Sound(constants.BACKGROUND_MUSIC)
sounds.set_volume(0.5)
play_sound.PlaySounds(sounds)


while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	if not theship.handle_event(event):
		pass #todo: handle events the ship isn't interested in

	level.step(scrollPosition)

	# do some network stuff
	for o in level.physicalObjectsExternalRemoveList:
		removeQueue.append(o.networkID)

	screen.fill(pygame.Color('black'))
	movedlevelrect.y = -scrollPosition;
	screen.blit(level.image, movedlevelrect)
	for o in level.physicalObjects:
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

	for netid in removeQueue:
		network.sendIntData( conn, Message.DESTROYOBJ )
		network.sendIntData( conn, netid )
	removeQueue = []

	for o in level.physicalObjects[:]:
		if o.networkID == None:
			network.sendIntData( conn, Message.NEWOBJ )
			lastNetworkID = lastNetworkID + 1
			o.networkID = lastNetworkID
			network.sendData( conn, struct.pack( "ii", o.typ, o.networkID ) )

		network.sendIntData( conn, Message.OBJSYNC )
		network.sendData( conn, struct.pack( "iffff", o.networkID, o.getX(), o.getY(), o.getVX(), o.getVY() ) )

conn.close()
