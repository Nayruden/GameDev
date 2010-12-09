import sys
import pygame
from pygame import mixer
from pygame.mixer import Sound
import constants


class PlaySounds:	
	pygame.mixer.init(44100,-16,300, 1024) #initialize mixer
	background = pygame.mixer.Channel(1)
	pygame.mixer.set_reserved(1)
	def __init__(self, sound, numberCheck):		
		if numberCheck == 0:
			self.background.play(sound)
		elif numberCheck == 1 or numberCheck == 3:	
			if self.background.get_busy():
				self.background.fadeout(1000)
				self.background.play(sound)					
		else:
			openChannel = pygame.mixer.find_channel()	#find open channel
			if openChannel:
				openChannel.play(sound) #play sound on open channel
			else:
				print "BUG: No open channel."	