# An adaption of Mario Code by Maarten Hus found at http://huscorp.nl/tag/pygame/
import pygame
import mario
import level
import tiles

screen = pygame.display.set_mode((624, 480)) #336, 432))
pygame.display.set_caption("Tyrian Defense")
clock = pygame.time.Clock()

level = level.Level()
mario = mario.Mario((250, 355), level)

movedlevelrect = level.rect.move(0,-level.yoffset)
running = True

while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
	
	mario.handle_event(event)
	mario.handle_animation()
			
	screen.fill(pygame.Color('black'))	
	screen.blit(level.image, movedlevelrect)
	screen.blit(mario.image, mario.rect, mario.area)

	pygame.display.flip()		
	clock.tick(60)
	
	#scroll the level down
	movedlevelrect = movedlevelrect.move(0,1)
	
	