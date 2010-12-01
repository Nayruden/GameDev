import sys
import pygame
from pygame import mixer
from pygame.mixer import Sound
import constants


class PlaySounds:	
	pygame.mixer.init(44100,-16,16, 1024) #initialize mixer
	def __init__(self, sound):		
		openChannel = pygame.mixer.find_channel()	#find open channel		
		openChannel.play(sound) #play sound on open channel
		
	