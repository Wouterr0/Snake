import os
import sys

from PIL import Image
import pygame


def surface_to_PIL(surface):
	raw_str = pygame.image.tostring(surface, "RGBA", False)
	surface = Image.frombytes("RGBA", surface.get_size(), raw_str)
	return surface


def PIL_to_surface(surface):
	raw_str = surface.tobytes("raw", "RGBA")
	surface = pygame.image.fromstring(raw_str, surface.size, "RGBA")
	return surface



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
width, height = 800, 800
win = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption("Snake!")

# Load resources
apple_image = Image.open("resources/apple.png")



# Define gamespeed
gamespeed = 10


fpsClock = pygame.time.Clock()

def roundToNearestMultiple(number, multiple):
	return number - (number%multiple)

def unique(num_list):
	seen = []
	for i in num_list:
		if i not in seen:
			seen.append(i)
		else:
			return False
	return True

def updateWindow():
	'''
	This function checks if the player has quited the game so the pygame window exits instead of crash. Also this function updates the window and handles the resizing of the window. This function needs to be executed every game tick.
	'''
	global width, height
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			sys.exit(0)
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit(0)
		elif event.type == pygame.VIDEORESIZE:
				width, height = event.size
				if debug:
					print('[*] resizing to', width, height)

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