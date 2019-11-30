import os
import sys
import colorsys

from PIL import Image, ImageEnhance
import numpy as np
import pygame


def surface_to_PIL(surface):
	raw_str = pygame.image.tostring(surface, "RGBA", False)
	surface = Image.frombytes("RGBA", surface.get_size(), raw_str)
	return surface

def PIL_to_surface(surface):
	raw_str = surface.tobytes("raw", "RGBA")
	surface = pygame.image.fromstring(raw_str, surface.size, "RGBA")
	return surface

def changeBrightness(image, brightness):
	return ImageEnhance.Brightness(image).enhance(brightness)

def combineSufacesVertical(img1, img2):
	img1 = surface_to_PIL(img1)
	img2 = surface_to_PIL(img2)
	dst = Image.new("RGBA", (max(img1.width, img2.width), img1.height+img2.height))
	dst.paste(img1, ((dst.width-img1.width)//2, 0))					# (dst.width-img1.width)//2 to make sure the image is centered
	dst.paste(img2, ((dst.width-img2.width)//2, img1.height))
	return PIL_to_surface(dst)

def repeatTileImage(img, size):
	result = Image.new(img.mode, size)
	for i in range(0, size[0], img.width):
		for j in range(0, size[1], img.height):
			result.paste(img, (i, j))
	return result


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


def mapArrayToRainBow(arr, length):
	new = np.zeros((*arr.shape, 3))
	new[:,0] = arr															# Make a new array in the RGB shape (..., 3)
	for i in range(len(arr)):
		new[i] = np.array(colorsys.hsv_to_rgb(new[i][0], 1-(1/length), 1-(1/length)))*255			# Convert hue to RGB
	new = np.array(new, dtype=np.uint8)
	return new.tolist()
	

# Debug mode
debug = True

# Screen settings
width, height = 800, 800

# Game Font
gameFont = "FSEX300.ttf"

# Start settings
startBgImage = Image.open("assets/brick.png")

# Grid settings
gridColor = (np.random.randint(0, 256), np.random.randint(0, 256), np.random.randint(0, 256))
gridBorderColor = (np.array(gridColor)*0.7).tolist()

# Apple settings
appleImage = Image.open("assets/apple.png")

# Snake settings
initSnakeLength = 4
snakeHeadImage = Image.open("assets/snakeHead.png")


# Define gamespeed
gamespeed = 10



# Define common colors
WHITE = (255, 255, 255)
GREY = (127, 127, 127)
BLACK = (0, 0, 0)
FUCHSIA = (255, 0, 255)
RED = (255, 0, 0)
ORANGE = (255, 127, 0)
JELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
AQUA = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 255)
DARK_RED = (127, 0, 0)
DARK_GREEN = (0, 127, 0)
DARK_BLUE = (0, 0, 127)
LIGHT_RED = (255, 127, 127)
LIGHT_GREEN = (127, 255, 127)
LIGHT_BLUE = (127, 127, 255)