import sys
import pygame
from pygame import mixer
from pygame.mixer import Sound
import constants


class PlaySounds:	
	pygame.mixer.init(44100,-16,300, 1024) #initialize mixer
	def __init__(self, sound):		
		openChannel = pygame.mixer.find_channel()	#find open channel
		if openChannel:
			openChannel.play(sound) #play sound on open channel
		else:
			print "BUG: No open channel."
		
	