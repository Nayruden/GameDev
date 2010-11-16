# An adaption of Mario Code by Maarten Hus found at http://huscorp.nl/tag/pygame/
import pygame
import level
import tiles
import ship

screen = pygame.display.set_mode((624, 480)) #336, 432))
pygame.display.set_caption("Tyrian Defense")
clock = pygame.time.Clock()

level = level.Level()
ship = ship.Ship((250, 355), level,pygame.rect.Rect(level.rect.x,level.rect.y,level.rect.width,480))

movedlevelrect = level.rect.move(0,-level.yoffset)
running = True

while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
	
	if not ship.handle_event(event):
		pass #todo: handle events the ship isn't interested in
	
	ship.step()
			
	screen.fill(pygame.Color('black'))	
	screen.blit(level.image, movedlevelrect)
	screen.blit(ship.image, ship.rect, ship.area)

	pygame.display.flip()		
	clock.tick(60)
	
	#scroll the level down
	movedlevelrect = movedlevelrect.move(0,1)
	
	