import os
import sys

import pygame


# Initialize Pygame
pygame.init()

# Clear debug cmd prompt
os.system("cls")

# Debug mode
debug = True

# Print started
if debug:
	print("<--------------------------------------------- BEGIN --------------------------------------------->")

# Screen settings
width, height = 1200, 800
win = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption("Snake!")

fpsClock = pygame.time.Clock()


def updateWindow():
	'''
	This function checks if the player has quited the game so the pygame window exits instead of crash. Also this function updates the window and handles the resizing of the window. This function needs to be executed every game tick.
	'''
	global width, height
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			sys.exit(0)
		if event.type == pygame.QUIT:
			sys.exit(0)
		elif event.type == pygame.VIDEORESIZE:
				width, height = event.size
				if debug:
					print('resizing to', width, height)

	pygame.display.update()



# Define common colors
WHITE = (255, 255, 255, 255)
GREY = (127, 127, 127, 255)
BLACK = (0, 0, 0, 255)
FUCHSIA = (255, 0, 255, 255)
RED = (255, 0, 0, 255)
ORANGE = (255, 127, 0, 255)
JELLOW = (255, 255, 0, 255)
GREEN = (0, 255, 0, 255)
AQUA = (0, 255, 255, 255)
BLUE = (0, 0, 255, 255)
PURPLE = (255, 0, 255, 255)
DARK_RED = (127, 0, 0, 255)
DARK_GREEN = (0, 127, 0, 255)
DARK_BLUE = (0, 0, 127, 255)
LIGHT_RED = (255, 127, 127, 255)
LIGHT_GREEN = (127, 255, 127, 255)
LIGHT_BLUE = (127, 127, 255, 255)