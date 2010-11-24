import socket
import pickle
import pygame
import level
import tiles
import ship
import constants
import network

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
theship = ship.Ship((constants.SCREEN_WIDTH/2, level.rect.height - 60), level, Rect(level.rect.x,level.rect.y,level.rect.width,constants.SCREEN_HEIGHT))

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

	theship.step(scrollPosition)

	screen.fill(pygame.Color('black'))
	movedlevelrect.y = -scrollPosition;
	screen.blit(level.image, movedlevelrect)
	screen.blit(theship.image, Rect((theship.rect.x, theship.rect.y - scrollPosition),(theship.rect.width, theship.rect.height)), theship.area)

	pygame.display.flip()
	clock.tick(60)

	#scroll the level down
	scrollPosition -= constants.SCROLL_RATE
	#movedlevelrect = movedlevelrect.move(0,SCROLL_RATE)

conn.close()
